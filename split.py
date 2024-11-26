import math
import re

def split_wire_with_tl(wire, z0, delay_per_unit, units_per_split):
    """
    Splits a wire into multiple segments with transmission lines between.

    :param wire: A string defining the wire in Xschem format (e.g., 'N x1 y1 x2 y2 {lab=#net6}')
    :param z0: Characteristic impedance for the transmission line.
    :param delay_per_unit: Delay per unit length.
    :param units_per_split: Length in units after which to insert a transmission line.
    :return: A string with the updated wires and transmission lines.
    """

    # Parse the wire input
    pattern = r'N\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\{.+\}'
    match = re.match(pattern, wire)
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
    num_splits = math.floor(wire_length / units_per_split) - 1
    remainder_length = wire_length % units_per_split
    num_transmission_lines = num_splits + (remainder_length > 0)

    if num_transmission_lines == 0:
        return wire

    transmission_line_delay = delay_per_unit * wire_length / num_transmission_lines

    output = []

    # Left to Right
    if x1 < x2 and y1 == y2:
        current_x = x1
        for i in range(num_transmission_lines):
            next_x = current_x + units_per_split-1
            output.append(f'N {current_x} {y1} {next_x} {y1} {{}}')
            current_x = next_x
            output.append(f'C {{xschem/tl_point.sym}} {current_x} {y1} 0 0 {{name=T{i + 1} nam=VGND nbm=VGND z0={z0} td={transmission_line_delay}}}')
            current_x += 1

        if remainder_length > 0:
            output.append(f'N {current_x} {y1} {x2} {y1} {{}}')

    # Down to Up
    elif x1 == x2 and y1 < y2:
        current_y = y1
        for i in range(num_transmission_lines):
            next_y = current_y + units_per_split-1
            output.append(f'N {x1} {current_y} {x1} {next_y} {{}}')
            current_y = next_y
            output.append(f'C {{xschem/tl_point.sym}} {x1} {current_y} 1 0 {{name=T{i + 1} nam=VGND nbm=VGND z0={z0} td={transmission_line_delay}}}')
            current_y += 1

        if remainder_length > 0:
            output.append(f'N {x1} {current_y} {x1} {y2} {{}}')

    # Unsupported directions
    else:
        raise ValueError("Unsupported wire direction.")

    return '\n'.join(output)


if __name__=='__main__':
    # Example usage
    wire = "N -510 190 -140 190 {lab=#net6}"
    # wire = "N -140 190 -510 190 {lab=#net6}"
    # wire = "N -680 190 -680 500 {lab=#net1}"
    # wire = "N -680 500 -680 190 {lab=#net1}"

    z0 = 50
    delay_per_unit = 1
    units_per_split = 308

    result = split_wire_with_tl(wire, z0, delay_per_unit, units_per_split)
    print(result)
