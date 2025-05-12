
import re
import os, sys
import subprocess

import numpy as np
import matplotlib.pyplot as plt
import json

import re
from collections import OrderedDict
from typing import Dict, List, Tuple, Any


class Xschem3D:
    WIRE_REGEX = r'N\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\{.+\}'
    cell_instance_name = "X1"


    def sch2nets(self):
        wire_pattern = re.compile(
            r"^N\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\{lab=#?([^}]+)\}$"
        )
        port_pattern = re.compile(
            r"^C\s+\{(ipin|opin)\.sym\}\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+\{name=[^ ]+\s+lab=([^}]+)\}$"
        )
        power_ports = {"VGND", "VNB", "VPB", "VPWR"}

        nets = OrderedDict()

        # First pass: record port nets in file order
        with open(self.schematic_filename, 'r') as f:
            for line in f:
                m = port_pattern.match(line.strip())
                if m:
                    pin_type, label = m.groups()
                    if label not in nets:
                        nets[label] = {'voltages': [], 'wires': [], 'nettype': 'internal'}

                    if label in power_ports:
                        nets[label]['nettype'] = 'power'
                    elif pin_type == 'ipin':
                        nets[label]['nettype'] = 'input_port'
                    elif pin_type == 'opin':
                        nets[label]['nettype'] = 'output_port'
                    else:
                        raise ValueError(f"Unknown pin type '{pin_type}' for net '{label}'")

        # Second pass: record wire nets in file order, creating new entries if needed
        with open(self.schematic_filename, 'r') as f:
            for line in f:
                m = wire_pattern.match(line.strip())
                if m:
                    x1, y1, x2, y2, label = m.groups()
                    if label not in nets:
                        nets[label] = {'voltages': [], 'wires': [], 'nettype': 'internal'}
                    coords = (int(x1), int(y1), int(x2), int(y2))
                    nets[label]['wires'].append(coords)

        return nets


    def xschem_symbol_params2dict(param_str):
        result = {}
        tokens = re.split(r'\s+', param_str.strip())
        for token in tokens:
            if not token:
                continue
            if '=' not in token:
                raise ValueError(f"Malformed param string. Found {token}")
            key, val = token.split('=', 1)
            result[key] = val
        return result


    def sch2fets(self):
        symbol_pattern = re.compile(
            r"^C\s+\{(.+?)\}\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\{([\s\S]*?)\}$",
            re.MULTILINE
        )

        with open(self.schematic_filename, 'r') as f:
            content = f.read()

        fets = []
        for match in symbol_pattern.finditer(content):
            symbol_path = match.group(1)
            x_coord     = int(match.group(2))
            y_coord     = int(match.group(3))
            rotate      = int(match.group(4))
            flip        = int(match.group(5))
            parameters  = Xschem3D.xschem_symbol_params2dict(match.group(6))
            if 'pfet' in symbol_path.lower():
                fettype = 'pfet'
            elif 'nfet' in symbol_path.lower():
                fettype = 'nfet'
            else:
                continue
            model_name = f"{symbol_path.split('/')[0]}__{parameters['model']}"
            fet = {
                'name':                f'{parameters["spiceprefix"]}{parameters["name"]}',
                'type':                fettype,
                'location':            [x_coord, y_coord],
                'rotate_clockwise':    90 * rotate,
                'flip':                bool(flip),
                'current_vector_name': f'@M.{Xschem3D.cell_instance_name}.{parameters["spiceprefix"]}{parameters["name"]}.M{model_name}[id]',
                'currents':            []
            }
            fets.append(fet)
        return fets


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
        self.nets = self.sch2nets()
        self.fets = self.sch2fets()

    def schematic_basename(self):
        return os.path.basename(self.schematic_filename)

    def xschemrc_filename(pdk="sky130A"):
        pdk_root = os.getenv('PDK_ROOT')
        if not pdk_root:
            raise EnvironmentError("PDK_ROOT environment variable is not set.")
        return os.path.join(os.getenv('PDK_ROOT'), f'{pdk}/libs.tech/xschem/xschemrc')


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
        return os.path.join(self.build_dir, "simdata.txt")

    def input_ports(self) -> List[str]:
        return [n for n, info in self.nets.items() if info['nettype'] == 'input_port']

    def output_ports(self) -> List[str]:
        return [n for n, info in self.nets.items() if info['nettype'] == 'output_port']

    def power_ports(self) -> List[str]:
        return [n for n, info in self.nets.items() if info['nettype'] == 'power']

    def all_ports(self) -> List[str]:
        return [n for n, info in self.nets.items() if info['nettype'] in {'input_port', 'output_port', 'power'}]

    def internal_nets(self) -> List[str]:
        return [n for n, info in self.nets.items() if info['nettype'] == 'internal']

    def ngspice_formatted_net_names(self) -> List[str]:
        out = self.all_ports()
        out.extend(f"{self.cell_instance_name}.{net}" for net in self.internal_nets())
        return out

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
            file.write(f'{Xschem3D.cell_instance_name} {" ".join(self.all_ports())} {model_name}\n')
            file.write(f'\n')
            file.write(f'.options savecurrents\n')
            file.write(f'\n')
            file.write(f'.control\n')
            file.write(f'    tran {self.time_precision} {self.tran_end_time()}\n')
            file.write(f'    wrdata {self.simdata_filename()} {" ".join(self.ngspice_formatted_net_names())} {" ".join(fet["current_vector_name"] for fet in self.fets)}\n')
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
            f"""
            SKYWATER_MODELS={Xschem3D.skywater_models(self.pdk)} \
            ngspice {self.testbench_filename()} {self.netlist_filename()}
            """,
            shell=True,
            check=True
        )


    def parse_simdata_file(filename):
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


    def _prune_redundant(time_value_pairs):
        if len(time_value_pairs) < 3:
            return time_value_pairs
        out = [time_value_pairs[0]]
        last_added_t, last_added_v = out[0]

        for i in range(1, len(time_value_pairs)-1):
            curr_t, curr_v = time_value_pairs[i]
            next_t, next_v = time_value_pairs[i+1]
            if not (last_added_v == curr_v == next_v):
                out.append(time_value_pairs[i])
                last_added_t, last_added_v = curr_t, curr_v

        out.append(time_value_pairs[-1])
        return out


    def load_simdata(self):
        net_names = self.ngspice_formatted_net_names()
        times, data = Xschem3D.parse_simdata_file(self.simdata_filename())
        for i, label in enumerate(net_names):
            # remove instance name
            while '.' in label:
                label = label.split('.', 1)[1]
            self.nets[label]['voltages'] = Xschem3D._prune_redundant(list(zip(times[i], data[i])))
        for i in range(len(self.fets)):
            self.fets[i]['currents'] = Xschem3D._prune_redundant(list(zip(times[i+len(net_names)], data[i+len(net_names)])))


    def plot_ports(self):
        plt.figure(figsize=(10, 6))
        for net, info in self.nets.items():
            if info['nettype'] in {'input_port', 'output_port'}:
                if not info['voltages']:
                    continue
                times, volts = zip(*info['voltages'])
                plt.plot(times, volts, label=net)

        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")
        plt.title("Net Voltages")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    def export_json(self, json_filename=None):
        if json_filename is None:
            json_filename = os.path.join(self.build_dir, 'circuit.json')

        circuit = {
            'nets': self.nets,
            'fets': self.fets
        }
        json.dump(circuit,
                  open(json_filename,'w'),
                  default=lambda o: o.tolist() if hasattr(o, 'tolist') else o,
                  indent=2)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Error: Incorrect number of arguments.")
        print(f"Usage: python3 {sys.argv[0]} <schematic_filename> <stimulus_filename> <build_dir>")
        sys.exit(1)

    schematic_filename = sys.argv[1]
    stimulus_filename = sys.argv[2]
    build_dir = sys.argv[3]

    if not os.path.isfile(schematic_filename):
        print(f"Error: Schematic file '{schematic_filename}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(stimulus_filename):
        print(f"Error: Stimulus file '{stimulus_filename}' does not exist.")
        sys.exit(1)

    circuit = Xschem3D(
        schematic_filename=schematic_filename,
        stimulus_filename=stimulus_filename,
        build_dir=build_dir)

    circuit.generate_simdata_files()
    circuit.load_simdata()
    circuit.export_json()
    # circuit.plot_ports()
