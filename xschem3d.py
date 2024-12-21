
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

    def __init__(self, schematic_filename, stimulus_filename,
                 to_split=True, meters_per_unit=1e-9, units_per_split=20,
                 time_precision='0.01ns', vdd=1.8, trisefall=20e-12,
                 cache_root="build/Xschem3D"):
        self.schematic_filename = schematic_filename
        self.stimulus_filename = stimulus_filename
        self.to_split = to_split
        self.meters_per_unit = meters_per_unit
        self.units_per_split = units_per_split
        self.time_precision = time_precision
        self.vdd = vdd
        self.trisefall = trisefall
        self.cache_root = cache_root

        self.TL_COUNTER = 0

        self.copy_stimulus_to_cache()
        self.copy_schematic_to_cache()

    def _hash(self):
        input_str = ""
        if self.to_split:
            input_str = f"{self.schematic_filename}{self.stimulus_filename}{self.to_split}{self.meters_per_unit}{self.units_per_split}{self.time_precision}{self.vdd}{self.trisefall}"
        else:
            input_str = f"{self.schematic_filename}{self.stimulus_filename}{self.to_split}{self.time_precision}{self.vdd}{self.trisefall}"
        return hashlib.sha256(input_str.encode()).hexdigest()

    def _cache_dir(self):
        return f'{self.cache_root}/{self._hash()}'

    def cached_stimulus_file(self):
        return os.path.join(self._cache_dir(), os.path.basename(self.stimulus_filename))

    def cached_netlist_file(self):
        extensionless_name, _ = os.path.splitext(self.cached_schematic_file())
        return os.path.join(extensionless_name + '.spice')

    def cached_schematic_file(self):
        return os.path.join(self._cache_dir(), os.path.basename(self.schematic_filename))

    def cached_split_schematic_file(self):
        return os.path.join(self._cache_dir(), 'split', os.path.basename(self.schematic_filename))

    def _copy_file_to_cache(self, source_file, cached_filename):
        if os.path.isabs(cached_filename):
            raise ValueError(f"The path '{cached_filename}' is not a relative path.")
        cached_filename = os.path.join(self._cache_dir(), os.path.basename(cached_filename))
        cached_filename_dir = os.path.dirname(cached_filename)
        if not os.path.exists(cached_filename_dir):
            os.makedirs(cached_filename_dir)
        shutil.copy(source_file, cached_filename)

    def _file_up_to_date(self, source_file, cached_filename):
        if os.path.isabs(cached_filename):
            raise ValueError(f"The path '{cached_filename}' is not a relative path.")
        if not os.path.exists(cached_filename):
            return False
        source_mtime = os.path.getmtime(source_file)
        dest_mtime = os.path.getmtime(cached_filename)
        return source_mtime <= dest_mtime

    def stimulus_up_to_date(self):
        cached_filename = os.path.basename(self.stimulus_filename)
        return self._file_up_to_date(self.stimulus_filename, cached_filename)

    def schematic_up_to_date(self):
        cached_filename = os.path.basename(self.schematic_filename)
        return self._file_up_to_date(self.schematic_filename, cached_filename)

    def copy_stimulus_to_cache(self):
        cached_filename = os.path.basename(self.stimulus_filename)
        if not self.stimulus_up_to_date():
            self._copy_file_to_cache(self.stimulus_filename, cached_filename)

    def copy_schematic_to_cache(self):
        cached_filename = os.path.basename(self.schematic_filename)
        if not self.schematic_up_to_date():
            self._copy_file_to_cache(self.schematic_filename, cached_filename)

    def remove_stimulus_children(self):
        for f in [os.path.basename(self.stimulus_filename)]:
            cached_file = os.path.join(self._cache_dir(), f)
            if os.path.exists(cached_file):
                os.remove(cached_file)

    def remove_schematic_children(self):
        for f in [os.path.basename(self.schematic_filename)]:
            cached_file = os.path.join(self._cache_dir(), f)
            if os.path.exists(cached_file):
                os.remove(cached_file)

    def cached_svg_file(self):
        extensionless_name, _ = os.path.splitext(self.cached_schematic_file())
        return os.path.join(extensionless_name + '.svg')

    def generate_svg(self):
        xschem_rcfile = os.path.join(os.getenv('PDK_ROOT'), 'sky130A/libs.tech/xschem/xschemrc')
        subprocess.run(f"SVG_NAME=\"{self.cached_svg_file()}\" SCH_NAME=\"{self.cached_schematic_file()}\" xschem --rcfile={xschem_rcfile} --no_x --script xschem/generate_svg.tcl --log \"{self.cached_svg_file()}.log\"", text=True, shell=True)


    def convert_time(t):
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
        with open(self.cached_stimulus_file(), 'r') as file:
            for line in file:
                if line.startswith('*') or line.strip() == '':
                    continue
                time = Xschem3D.convert_time(line.split()[0])
                final_time = max(final_time, time)
        return final_time

    def split_wire_with_tl(self, wire):
        match = re.match(Xschem3D.WIRE_REGEX, wire)
        if not match:
            raise ValueError("Invalid wire format. Expected 'N x1 y1 x2 y2 {...}'")

        x1, y1, x2, y2 = match.groups()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        # Calculate wire properties
        wire_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        num_segments = math.ceil(wire_length / self.units_per_split)
        segment_length = wire_length / num_segments

        output = []

        # Left to Right
        if x1 < x2 and y1 == y2:
            current_x = x1
            for _ in range(num_segments):
                self.TL_COUNTER += 1
                output.append(f'C {{xschem/tl_point.sym}} {current_x} {y1} 0 0 {{name=USPLITTER{self.TL_COUNTER} gnd=VGND l={segment_length*self.meters_per_unit}}}')
                current_x += 1
                next_x = min(current_x + self.units_per_split-1, x2)
                output.append(f'N {current_x} {y1} {next_x} {y1} {{}}')
                current_x = next_x

        # Down to Up
        elif x1 == x2 and y1 < y2:
            current_y = y1
            for _ in range(num_segments):
                self.TL_COUNTER += 1
                output.append(f'C {{xschem/tl_point.sym}} {x1} {current_y} 1 0 {{name=USPLITTER{self.TL_COUNTER} gnd=VGND l={segment_length*self.meters_per_unit}}}')
                current_y += 1
                next_y = min(current_y + self.units_per_split-1, y2)
                output.append(f'N {x1} {current_y} {x1} {next_y} {{}}')
                current_y = next_y

        # Unsupported directions
        else:
            raise ValueError("Unsupported wire direction.")

        return '\n'.join(output)


    def generate_split_schematic(self):
        if not self.schematic_up_to_date():
            self.remove_schematic_children()
            self.copy_schematic_to_cache()

        output_dir = os.path.dirname(self.cached_split_schematic_file())
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(self.cached_schematic_file(), 'r') as infile, open(self.cached_split_schematic_file(), 'w') as outfile:
            for line in infile:
                modified_line = re.sub(Xschem3D.WIRE_REGEX, lambda match: self.split_wire_with_tl(match.group(0)), line)
                outfile.write(modified_line)


    def generate_netlist_file(self):
        if self._file_up_to_date(self.schematic_filename, self.cached_netlist_file()):
            return

        if not self.schematic_up_to_date():
            self.remove_schematic_children()
            self.copy_schematic_to_cache()

        if self.to_split:
            self.generate_split_schematic()

        schematic_file = self.cached_schematic_file() if not self.to_split else self.cached_split_schematic_file()

        pdk_root = os.getenv('PDK_ROOT')
        if not pdk_root:
            raise EnvironmentError("PDK_ROOT environment variable is not set.")

        xschem_rcfile = os.path.join(os.getenv('PDK_ROOT'), 'sky130A/libs.tech/xschem/xschemrc')
        commands = f"""
            set netlist_dir {self._cache_dir()}
            xschem load {schematic_file}
            set netlist_type spice
            set lvs_netlist 1
            xschem netlist
            xschem exit closewindow force
            """

        subprocess.run(f"xschem --rcfile={xschem_rcfile} --no_x", input=commands, text=True, shell=True)


    def cached_sim_file(self):
        extensionless_name, _ = os.path.splitext(self.cached_schematic_file())
        return os.path.join(extensionless_name + '.sim.spice')

    def cached_ports_simdata_file(self):
        return os.path.join(self._cache_dir(), "ports.txt")

    def cached_splits_simdata_file(self):
        return os.path.join(self._cache_dir(), "splits.txt")

    def input_ports(self):
        return [port for port in self.all_ports() if port not in self.power_ports() and port not in self.output_ports()]

    def output_ports(self):
        with open(self.cached_schematic_file(), 'r') as file:
            lines = file.readlines()
            return [re.search(r"lab=([^}]+)", line).group(1) for line in lines if "{opin.sym}" in line]

    def power_ports(self):
        return ["VGND", "VNB", "VPB", "VPWR"]

    def all_ports(self):
        with open(self.cached_schematic_file(), 'r') as file:
            lines = file.readlines()
            return [re.search(r"lab=([^}]+)", line).group(1) for line in lines if "{ipin.sym}" in line or "{opin.sym}" in line]

    def generate_sim_file(self):
        if self._file_up_to_date(self.schematic_filename, self.cached_sim_file()):
            return

        if not self.schematic_up_to_date():
            self.remove_schematic_children()
            self.copy_schematic_to_cache()
        if not self.stimulus_up_to_date():
            self.remove_stimulus_children()
            self.copy_stimulus_to_cache()

        self.generate_netlist_file()

        model_name = os.path.splitext(os.path.basename(self.schematic_filename))[0]

        with open(self.cached_sim_file(), 'w') as file:
            file.write(f'.lib "$SKYWATER_MODELS/sky130.lib.spice" tt\n')
            file.write(f'.nodeset all={self.vdd/2}\n')
            file.write(f'.model urcmod urc cperl=100p rperl=100k fmax=10G\n')
            file.write(f'\n')
            file.write(f'VVGND VGND 0 0\n')
            file.write(f'VVNB VNB 0 0\n')
            file.write(f'VVPB VPB 0 {self.vdd}\n')
            file.write(f'VVPWR VPWR 0 {self.vdd}\n')
            file.write(f'\n')
            file.write(f'.model digital_stimulus d_source(input_file="{self.cached_stimulus_file()}")\n')
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
            file.write(f'    wrdata {self.cached_ports_simdata_file()} {" ".join(self.all_ports())}\n')
            if self.to_split:
                file.write(f'    wrdata {self.cached_splits_simdata_file()} {" ".join(self.nets_connected_to_splitters())}\n')
            file.write(f'    exit\n')
            file.write(f'.endc\n')
            file.write(f'\n')
            file.write('.end\n')



    def generate_simdata_files(self):
        # Check if the simulation data file is up-to-date
        if self._file_up_to_date(self.schematic_filename, self.cached_ports_simdata_file()):
            return

        # Ensure the schematic and stimulus files are up-to-date
        if not self.schematic_up_to_date():
            self.remove_schematic_children()
            self.copy_schematic_to_cache()
        if not self.stimulus_up_to_date():
            self.remove_stimulus_children()
            self.copy_stimulus_to_cache()

        # Generate the simulation file (if not already generated)
        self.generate_sim_file()

        # Set the required environment variables
        pdk = "sky130A"
        pdk_root = os.getenv('PDK_ROOT')  # Assuming the PDK_ROOT is set in the environment
        if pdk_root is None:
            raise ValueError("Environment variable PDK_ROOT is not set.")

        skywater_models = os.path.join(pdk_root, pdk, 'libs.tech', 'combined')

        # Run the ngspice simulation with the appropriate environment variables
        subprocess.run(
            f"export PDK={pdk} && export SKYWATER_MODELS={skywater_models} && ngspice {self.cached_sim_file()} {self.cached_netlist_file()}",
            shell=True,
            check=True  # Ensure the subprocess call raises an error if it fails
        )



    def parse_simdata_file(self, filename):
        self.generate_simdata_files()

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
        plt.figure(figsize=(10, 6))

        all_ports = self.all_ports()
        times, datasets = self.parse_simdata_file(self.cached_ports_simdata_file())
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


    def get_splitter_info(self):
        if not self.to_split:
            raise ValueError('Splitting disabled.')

        self.generate_netlist_file()

        splitter_info = {}
        all_ports = self.all_ports()
        with open(self.cached_netlist_file(), 'r') as file:
            for line in file:
                parts = line.split()
                if parts and parts[0].startswith('USPLITTER'):
                    if len(parts) > 2:
                        nets = []
                        for n in [parts[1], parts[2]]:
                            if n in all_ports:
                                nets.append(n)
                            else:
                                nets.append(f'x1.{n}')
                        splitter_info[parts[0]] = {'nets': nets}

        with open(self.cached_split_schematic_file(), 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 6 and parts[0] == 'C' and parts[1] == '{xschem/tl_point.sym}':
                    x, y = int(parts[2]), int(parts[3])
                    # Extract name
                    name = None
                    attributes = ' '.join(parts[6:]).strip('{}').split()
                    for a in attributes:
                        if a.startswith('name='):
                            name = a.split('=')[1]
                            break
                    if name and name in splitter_info:
                        splitter_info[name]['coordinates'] = (x, y)

        return splitter_info

    def nets_connected_to_splitters(self):
        splitter_info = self.get_splitter_info()
        split_nets = set()
        for info in splitter_info.values():
            split_nets.update(info['nets'])
        return sorted(split_nets)


    def cached_coordinate_voltages_file(self):
        return os.path.join(self._cache_dir(), 'coordinate_voltages.json')


    def generate_coordinate_voltages_file(self):
        times, datasets = self.parse_simdata_file(self.cached_splits_simdata_file())
        split_nets = self.nets_connected_to_splitters()
        net_voltages = {}
        for i, (time, data) in enumerate(zip(times, datasets)):
            net_voltages[split_nets[i]] = {"time": time, "voltages": data}

        splitter_info = self.get_splitter_info()

        coordinate_voltages = {}
        for tl in splitter_info:
            net1_voltages = net_voltages[splitter_info[tl]['nets'][0]]['voltages']
            net1_time = net_voltages[splitter_info[tl]['nets'][0]]['time']
            net2_voltages = net_voltages[splitter_info[tl]['nets'][1]]['voltages']
            net2_time = net_voltages[splitter_info[tl]['nets'][1]]['time']
            assert((net1_time == net2_time).all())
            avg_voltages = np.average([net1_voltages, net2_voltages], axis=0)

            coordinates_key = f"({splitter_info[tl]['coordinates'][0]}, {-splitter_info[tl]['coordinates'][1]})"
            coordinate_voltages[coordinates_key] = {"time": net1_time.tolist(), "voltages": avg_voltages.tolist()}

        with open(self.cached_coordinate_voltages_file(), 'w') as json_file:
            json.dump(coordinate_voltages, json_file, indent=4)





if __name__=='__main__':
    dfxtp = Xschem3D(
        schematic_filename="examples/dfxtp/sky130_fd_sc_hd__dfxtp_1.sch",
        stimulus_filename="examples/dfxtp/sky130_fd_sc_hd__dfxtp_1.stim",
        to_split=True)
    dfxtp.generate_coordinate_voltages_file()
    # dfxtp.plot_ports()
    dfxtp.generate_svg()
