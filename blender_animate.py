import bpy
import json
import sys

def delete_default_cube():
    if "Cube" in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['Cube']
        bpy.ops.object.delete()



def add_coordinate(times, voltages, coordinate):
    time_scalar = 1e12
    point_scalar = 7
    voltage_scalar = 2.5
    coordinate_scalar = 1/10
    fps = bpy.context.scene.render.fps
    frame_numbers = [int(t * fps * time_scalar) for t in times]

    x, y = coordinate
    x, y = x * coordinate_scalar, y * coordinate_scalar
    bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, 0))
    obj = bpy.context.object

    obj.scale = (point_scalar * coordinate_scalar, point_scalar * coordinate_scalar, point_scalar * coordinate_scalar)

    material = bpy.data.materials.new(name="VoltageMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]

    def voltage_to_color(voltage):
        r = min(voltage / 1.8, 1.0)
        g = 0.0
        b = max(1.8 - voltage, 0.0) / 1.8
        return (r, g, b, 1.0)

    obj.data.materials.append(material)
    for frame, voltage in zip(frame_numbers, voltages):
        color = voltage_to_color(voltage)
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Base Color"].keyframe_insert(data_path="default_value", frame=frame)

        obj.location.z = voltage * point_scalar * voltage_scalar * coordinate_scalar
        obj.keyframe_insert(data_path="location", frame=frame)



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

    if active_obj:
        active_obj.scale = (scale, scale, scale)
        active_obj.location = (location[0], location[1], active_obj.location.z)



def generate_blender_project(simulation_json, schematic_svg):
    delete_default_cube()
    add_schematic(schematic_svg, 492, (-86.585, 26.066))

    with open(simulation_json, 'r') as file:
        data = json.load(file)

    for coord_str, values in data.items():
        coord = tuple(map(int, coord_str.strip("()").split(", ")))
        times = values["time"]
        voltages = values["voltages"]
        add_coordinate(times, voltages, coord)



if __name__ == "__main__":
    simulation_json = sys.argv[-2]
    schematic_svg = sys.argv[-1]

    generate_blender_project(simulation_json, schematic_svg)
