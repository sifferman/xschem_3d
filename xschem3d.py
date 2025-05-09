
import re
import os
import subprocess
import math
import shutil
import hashlib

import numpy as np
import matplotlib.pyplot as plt
import json


class Xschem3D:
    WIRE_REGEX = r'N\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\{.+\}'

    def __init__(self, schematic_filename, stimulus_filename, pdk="sky130A", build_dir="build",
                 time_precision='0.01ns', vdd=1.8, trisefall=20e-12):
        self.schematic_filename = schematic_filename
        self.stimulus_filename = stimulus_filename
        self.pdk = pdk
        self.stimulus_filename
        self.build_dir = build_dir
        os.makedirs(build_dir, exist_ok=True)
        self.time_precision = time_precision
        self.vdd = vdd
        self.trisefall = trisefall

    def schematic_basename(self):
        return os.path.basename(self.schematic_filename)

    def svg_filename(self):
        extensionless_name, _ = os.path.splitext(self.schematic_basename())
        filename = os.path.join(self.build_dir, extensionless_name + '.svg')
        return filename

    def xschemrc_filename(pdk="sky130A"):
        pdk_root = os.getenv('PDK_ROOT')
        if not pdk_root:
            raise EnvironmentError("PDK_ROOT environment variable is not set.")
        return os.path.join(os.getenv('PDK_ROOT'), f'{pdk}/libs.tech/xschem/xschemrc')

    def generate_svg(self):
        export_dir_path = os.path.dirname(self.svg_filename())
        os.makedirs(export_dir_path, exist_ok=True)

        subprocess.run(
            f"SVG_NAME=\"{self.svg_filename()}\" "
            f"SCH_NAME=\"{self.schematic_filename}\" "
            f"xschem --rcfile={Xschem3D.xschemrc_filename(self.pdk)}"
            f"       --no_x "
            f"       --script xschem/generate_svg.tcl"
            f"       --log \"{self.svg_filename()}.log\"",
            text=True, shell=True)


    def netlist_filename(self):
        extensionless_name, _ = os.path.splitext(self.schematic_basename())
        filename = os.path.join(self.build_dir, extensionless_name + '.spice')
        return filename

    def generate_netlist(self):
        xschem_script = f"""
            set netlist_dir {self.build_dir}
            xschem load {self.schematic_filename}
            set netlist_type spice
            set lvs_netlist 1
            xschem netlist
            xschem exit closewindow force
            """
        command = f"""
            xschem --rcfile={Xschem3D.xschemrc_filename(self.pdk)} \\
                   --no_x
            """
        subprocess.run(
            command,
            input=xschem_script,
            text=True,
            shell=True)


    def simdata_filename(self):
        return os.path.join(self.build_dir, "ports.txt")

    def input_ports(self):
        return [port for port in self.all_ports() if port not in self.power_ports() and port not in self.output_ports()]

    def output_ports(self):
        with open(self.schematic_filename, 'r') as file:
            lines = file.readlines()
            return [re.search(r"lab=([^}]+)", line).group(1) for line in lines if "{opin.sym}" in line]

    def power_ports(self):
        return ["VGND", "VNB", "VPB", "VPWR"]

    def all_ports(self):
        with open(self.schematic_filename, 'r') as file:
            lines = file.readlines()
            return [re.search(r"lab=([^}]+)", line).group(1) for line in lines if "{ipin.sym}" in line or "{opin.sym}" in line]

    def timestring2float(t):
        si_prefixes = {
            't': 1.0e12,
            'g': 1.0e9,
            'me': 1.0e6,
            'k': 1.0e3,
            'u': 1.0e-6,
            'n': 1.0e-9,
            'p': 1.0e-12,
            'f': 1.0e-15,
            'a': 1.0e-18,
            'mi': 25.4e-6,
            'm': 1.0e-3
        }

        match = re.match(r"(\d+(\.\d+)?)([a-z]+)", t, re.IGNORECASE)
        if not match:
            raise ValueError("Input format is invalid. Expected a number followed by a prefix.")

        value_str, _, prefix = match.groups()
        value = float(value_str)

        scale_factor = 1.0
        for p in sorted(si_prefixes.keys(), key=len, reverse=True):
            if prefix.startswith(p):
                scale_factor = si_prefixes[p]
                break

        return value * scale_factor

    def tran_end_time(self):
        final_time = 0.0
        with open(self.stimulus_filename, 'r') as file:
            for line in file:
                if line.startswith('*') or line.strip() == '':
                    continue
                time = Xschem3D.timestring2float(line.split()[0])
                final_time = max(final_time, time)
        return final_time

    def testbench_filename(self):
        extensionless_name, _ = os.path.splitext(self.schematic_basename())
        return os.path.join(self.build_dir, extensionless_name + '_tb.spice')

    def generate_testbench(self):
        model_name = os.path.splitext(os.path.basename(self.schematic_filename))[0]

        with open(self.testbench_filename(), 'w') as file:
            file.write(f'.lib "$SKYWATER_MODELS/sky130.lib.spice" tt\n')
            file.write(f'.nodeset all={self.vdd/2}\n')
            file.write(f'\n')
            file.write(f'VVGND VGND 0 0\n')
            file.write(f'VVNB VNB 0 0\n')
            file.write(f'VVPB VPB 0 {self.vdd}\n')
            file.write(f'VVPWR VPWR 0 {self.vdd}\n')
            file.write(f'\n')
            file.write(f'.model digital_stimulus d_source(input_file="{self.stimulus_filename}")\n')
            file.write(f'a1 [{" ".join(port+"_DIGITAL" for port in self.input_ports())}] digital_stimulus\n')
            file.write(f'\n')
            file.write(f'.model dac_model dac_bridge(out_low=0 out_high={self.vdd} t_rise={self.trisefall} t_fall={self.trisefall})\n')
            for idx, port in enumerate(self.input_ports(), start=1):
                file.write(f'a_dac_bridge{idx} [{port}_DIGITAL] [{port}] dac_model\n')
            file.write(f'\n')
            file.write(f'X1 {" ".join(self.all_ports())} {model_name}\n')
            file.write(f'\n')
            file.write(f'.control\n')
            file.write(f'    tran {self.time_precision} {self.tran_end_time()}\n')
            file.write(f'    wrdata {self.simdata_filename()} {" ".join(self.all_ports())}\n')
            file.write(f'    exit\n')
            file.write(f'.endc\n')
            file.write(f'\n')
            file.write('.end\n')

    def skywater_models(pdk="sky130A"):
        pdk_root = os.getenv('PDK_ROOT')
        if not pdk_root:
            raise EnvironmentError("PDK_ROOT environment variable is not set.")
        return os.path.join(pdk_root, pdk, 'libs.tech', 'combined')

    def generate_simdata_files(self):
        self.generate_netlist()
        self.generate_testbench()
        subprocess.run(
            f"export PDK={self.pdk} && export SKYWATER_MODELS={Xschem3D.skywater_models(self.pdk)} && ngspice {self.testbench_filename()} {self.netlist_filename()}",
            shell=True,
            check=True
        )


    def parse_simdata_file(self, filename):
        times = []
        datasets = []

        with open(filename, 'r') as file:
            for line in file:
                values = np.array([float(x) for x in line.split()])
                time_values = values[::2]
                data_values = values[1::2]
                times.append(time_values)
                datasets.append(data_values)

        return np.array(times).T, np.array(datasets).T


    def plot_ports(self):
        self.generate_simdata_files()

        plt.figure(figsize=(10, 6))

        all_ports = self.all_ports()
        times, datasets = self.parse_simdata_file(self.simdata_filename())
        for i, (time, data) in enumerate(zip(times, datasets)):
            if all_ports[i] not in self.power_ports():
                plt.plot(time, data, label=all_ports[i])

        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")
        plt.title("Time vs Voltage")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__=='__main__':
    dfxtp = Xschem3D(
        schematic_filename="examples/dfxtp/sky130_fd_sc_hd__dfxtp_1.sch",
        stimulus_filename="examples/dfxtp/sky130_fd_sc_hd__dfxtp_1.stim")
    dfxtp.generate_svg()
    dfxtp.plot_ports()
