import bpy
import json
import sys
import mathutils
import math


def delete_default_cube():
    if "Cube" in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['Cube']
        bpy.ops.object.delete()


def add_schematic(schematic_svg, scale=1, location=(0,0)):
    bpy.ops.import_curve.svg(filepath=schematic_svg)

    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'CURVE':
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
    active_obj = bpy.context.view_layer.objects.active
    if active_obj:
        bpy.ops.object.join()
        active_obj.scale = (scale, scale, scale)
        active_obj.location = (location[0], location[1], active_obj.location.z)


def add_wire(name, start, end, times, voltages,
             voltage_scalar=0.01, time_scalar=1e9):
    """
    Create a cylinder representing a wire from start to end,
    and animate its radius based on voltages over time.
    - start, end: (x, y, z) tuples
    - times: list of time values (floats)
    - voltages: list of voltage values (floats)
    - voltage_scalar: factor to convert voltage to cylinder radius
    - time_scalar: factor to stretch time axis
    """
    vec = mathutils.Vector(end) - mathutils.Vector(start)
    length = vec.length

    # Create unit cylinder of depth=1
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, location=(0,0,0))
    wire = bpy.context.active_object
    wire.name = f"Wire_{name}_{start}_{end}"

    # Scale Z to match length
    wire.scale = (1, 1, length)

    # Orient cylinder along vec
    up = mathutils.Vector((0, 0, 1))
    rot_axis = up.cross(vec)
    if rot_axis.length > 1e-6:
        rot_axis.normalize()
        angle = up.angle(vec)
        quat = mathutils.Quaternion(rot_axis, angle)
        wire.rotation_mode = 'QUATERNION'
        wire.rotation_quaternion = quat

    # Position at midpoint
    midpoint = (mathutils.Vector(start) + mathutils.Vector(end)) / 2
    wire.location = midpoint

    fps = bpy.context.scene.render.fps
    for t, v in zip(times, voltages):
        frame = t * time_scalar * fps
        radius = max(v * voltage_scalar, 0)
        wire.scale.x = radius
        wire.scale.y = radius
        wire.keyframe_insert(data_path='scale', frame=frame, index=0)
        wire.keyframe_insert(data_path='scale', frame=frame, index=1)


def generate_blender_project(nets_json, schematic_svg,
                             voltage_scalar=0.01,
                             time_scalar=1e9,
                             wire_coord_scalar=1.0):
    delete_default_cube()
    add_schematic(schematic_svg, 49.2, (-8.6585, 2.6066))

    with open(nets_json, 'r') as file:
        data = json.load(file)

    for label, info in data.items():
        if not info.get('wires') or not info.get('voltages'):
            continue
        times, volts = zip(*info['voltages'])
        for wire_coords in info['wires']:
            x1, y1, x2, y2 = wire_coords
            # invert Y axis to match JSON coordinates
            start = (x1 * wire_coord_scalar,
                     -y1 * wire_coord_scalar,
                     0)
            end = (x2 * wire_coord_scalar,
                   -y2 * wire_coord_scalar,
                   0)
            add_wire(label, start, end, times, volts,
                     voltage_scalar=voltage_scalar,
                     time_scalar=time_scalar)


if __name__ == "__main__":
    args = sys.argv
    nets_json = args[-2]
    schematic_svg = args[-1]

    VOLTAGE_SCALAR = 0.05
    TIME_SCALAR = 20e9
    WIRE_COORD_SCALAR = 0.01  # adjust this to scale your net coordinates

    generate_blender_project(nets_json, schematic_svg,
                             voltage_scalar=VOLTAGE_SCALAR,
                             time_scalar=TIME_SCALAR,
                             wire_coord_scalar=WIRE_COORD_SCALAR)
