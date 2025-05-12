import bpy
import json
import sys
import mathutils
import math
import os
from bisect import bisect_right


def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.context.scene.frame_end = 1

    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'


def create_symbol_node_group(thickness, yscale, currents, gatebody_percentages, current_scalar, time_scalar):
    bpy.ops.mesh.primitive_cube_add()
    temp_obj = bpy.context.object
    bpy.ops.object.modifier_add(type='NODES')
    bpy.ops.node.new_geometry_node_group_assign()

    ng = bpy.data.node_groups.get("Geometry Nodes")
    ng.name = "Symbol from SVG"

    group_in = ng.nodes.get('Group Input')
    group_in.location = (-600, 0)
    group_out = ng.nodes.get('Group Output')
    group_out.location = (400, 0)

    quad = ng.nodes.new('GeometryNodeCurvePrimitiveQuadrilateral')
    quad.location = (-300, -100)
    quad.inputs["Width"].default_value = thickness
    quad.inputs["Height"].default_value = thickness

    c2m = ng.nodes.new('GeometryNodeCurveToMesh')
    c2m.location = (-50, 50)
    c2m.inputs[2].default_value = True # Fill Caps

    scale = ng.nodes.new('GeometryNodeScaleInstances')
    scale.location = (200, 50)
    scale.inputs["Scale"].default_value[1] = yscale

    set_mat = ng.nodes.new('GeometryNodeSetMaterial')
    set_mat.location = (300, -100)
    set_mat.inputs['Material'].default_value = create_fet_material(currents, gatebody_percentages, current_scalar, time_scalar)

    links = ng.links
    links.new(group_in.outputs["Geometry"], c2m.inputs["Curve"])
    links.new(quad.outputs["Curve"], c2m.inputs["Profile Curve"])
    links.new(c2m.outputs["Mesh"], scale.inputs["Instances"])
    links.new(scale.outputs["Instances"], set_mat.inputs["Geometry"])
    links.new(set_mat.outputs["Geometry"], group_out.inputs["Geometry"])

    bpy.data.objects.remove(temp_obj, do_unlink=True)

    return ng


def add_symbol(svg_path, scale, location, rotate_clockwise, flip, thickness, yscale, currents, gatebody_percentages, current_scalar, time_scalar):
    if not os.path.isabs(svg_path):
        absolute_svg_path = os.path.join(os.getcwd(), svg_path)
    else:
        absolute_svg_path = svg_path

    # Import SVG as grease pencil
    bpy.ops.wm.grease_pencil_import_svg(filepath=absolute_svg_path)
    obj = bpy.context.object

    obj.location = (location[0], -location[1], 0)
    obj.scale = (
        -scale if flip else scale,
        scale,
        scale
    )
    obj.rotation_euler.z = -math.radians(rotate_clockwise)

    # Lie flat
    obj.rotation_euler.x = -math.pi / 2

    node_group = create_symbol_node_group(thickness, yscale, currents, gatebody_percentages, current_scalar, time_scalar)
    geo_mod = obj.modifiers.new(name="SymbolNodes", type='NODES')
    geo_mod.node_group = node_group

    return obj


def create_fet_material(currents, gatebody_percentages, current_scalar, time_scalar):
    mat = bpy.data.materials.new(name="FetMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for n in nodes:
        nodes.remove(n)

    out = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = -200, 0
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    times_red = [t for t,_ in currents]
    vals_red = [v*current_scalar for _,v in currents]
    times_gb = [t for t,_ in gatebody_percentages]
    vals_gb = [v for _,v in gatebody_percentages]
    all_times = sorted(set(times_red + times_gb))

    fps = bpy.context.scene.render.fps

    def red_value(t):
        if t <= times_red[0]:
            return vals_red[0]
        elif t >= times_red[-1]:
            return vals_red[-1]
        else:
            idx = bisect_right(times_red, t)
            return vals_red[idx]

    def green_value(t):
        if t <= times_gb[0]:
            gb = vals_gb[0]
        elif t >= times_gb[-1]:
            gb = vals_gb[-1]
        else:
            idx = bisect_right(times_gb, t)
            gb = vals_gb[idx]
        threshold_percent = 0.3
        dimmer = 0.6
        return (1.0 - dimmer) * max(gb - 3*red_value(t) - threshold_percent, 0.0) / (1.0 - threshold_percent)

    for t in all_times:
        frame = t * time_scalar * fps

        r = red_value(t)
        g = green_value(t)

        r = min(max(r, 0.0), 1.0)
        g = min(max(g, 0.0), 1.0)

        bsdf.inputs['Base Color'].default_value = (r, g, 0.0, 1.0)
        bsdf.inputs['Base Color'].keyframe_insert(data_path='default_value', frame=frame)

    return mat


def create_wire_material(obj):
    mat = bpy.data.materials.new(name="WireMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs[27].default_value = (1, 0.672734, 0.0763408, 1)
        bsdf.inputs[28].default_value = 8
    return mat


def add_wire(net_name, start, end, voltages, voltage_scalar, time_scalar):
    vec = mathutils.Vector(end) - mathutils.Vector(start)
    length = vec.length

    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, location=(0,0,0))
    wire = bpy.context.active_object
    wire.name = f"Wire_{net_name}_{start}_{end}"

    wire.scale = (1, 1, length)
    up = mathutils.Vector((0, 0, 1))
    rot_axis = up.cross(vec)
    if rot_axis.length > 1e-6:
        rot_axis.normalize()
        angle = up.angle(vec)
        wire.rotation_mode = 'QUATERNION'
        wire.rotation_quaternion = mathutils.Quaternion(rot_axis, angle)

    midpoint = (mathutils.Vector(start) + mathutils.Vector(end)) / 2
    wire.location = midpoint

    mat = create_wire_material(wire)
    wire.data.materials.append(mat)

    fps = bpy.context.scene.render.fps
    for t, v in voltages:
        frame = int(t * time_scalar * fps)
        radius = max(v * voltage_scalar, 0)
        wire.scale.x = radius
        wire.scale.y = radius
        wire.keyframe_insert(data_path='scale', frame=frame, index=0)
        wire.keyframe_insert(data_path='scale', frame=frame, index=1)
        if frame > bpy.context.scene.frame_end:
            bpy.context.scene.frame_end = frame


def enable_fog_glow():
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    for node in list(tree.nodes):
        tree.nodes.remove(node)

    rl = tree.nodes.new(type='CompositorNodeRLayers'); rl.location = (0,200)
    glare = tree.nodes.new(type='CompositorNodeGlare'); glare.location = (200,200)
    glare.glare_type = 'FOG_GLOW'; glare.quality = 'MEDIUM'; glare.size = 6
    comp = tree.nodes.new(type='CompositorNodeComposite'); comp.location = (400,200)

    links = tree.links
    links.new(rl.outputs['Image'], glare.inputs['Image'])
    links.new(glare.outputs['Image'], comp.inputs['Image'])


def generate_blender_project(nets_json, voltage_scalar, current_scalar, time_scalar):
    reset_scene()

    with open(nets_json, 'r') as f:
        data = json.load(f)

    for label, info in data['nets'].items():
        if not info.get('wires') or not info.get('voltages'):
            continue
        voltages = info['voltages']
        for x1, y1, x2, y2 in info['wires']:
            start = (x1, -y1, 0)
            end = (x2, -y2, 0)
            add_wire(label, start, end, voltages,
                     voltage_scalar=voltage_scalar,
                     time_scalar=time_scalar)

    for fet in data['fets']:
        currents = fet['currents']
        add_symbol(svg_path=f'blender/{fet.get("type")}.svg',
                   scale=450, location=fet.get('location'),
                   rotate_clockwise=fet.get('rotate_clockwise'),
                   flip=fet.get('flip'),
                   thickness=40, yscale=8,
                   gatebody_percentages=fet.get('gatebody_percentages'), currents=currents,
                   current_scalar=current_scalar, time_scalar=time_scalar)

    enable_fog_glow()


if __name__ == '__main__':
    nets_json = sys.argv[-1]
    generate_blender_project(nets_json, voltage_scalar=3.0, current_scalar=5e3, time_scalar=5e9)
