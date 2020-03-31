import bpy
import bmesh
import math


def convert_2d_to_3d(obj, dimensions, point):
    display_size = obj.empty_display_size
    size_scale = display_size / dimensions[1]

    # 3D
    location_x = obj.location.x
    location_y = obj.location.y
    location_z = obj.location.z
    # 2D
    offset_x = (obj.empty_image_offset[0] + 0.5) * display_size
    offset_y = (obj.empty_image_offset[1] + 0.5) * display_size

    # 3D
    center_x = location_x + offset_x - display_size / 2
    center_y = location_y
    center_z = location_z + offset_y + size_scale * dimensions[0] / 2

    # 2D
    contour_x = point[0] * size_scale
    contour_y = point[1] * size_scale

    # 3D
    final_x = center_x + contour_x
    final_y = center_y
    final_z = center_z - contour_y

    return (final_x, final_y, final_z)


def convert_3d_to_2d(obj, dimensions, point):
    display_size = obj.empty_display_size
    size_scale = display_size / dimensions[1]

    # 3D
    location_x = obj.location.x
    location_z = obj.location.z
    # 2D
    offset_x = (obj.empty_image_offset[0] + 0.5) * display_size
    offset_y = (obj.empty_image_offset[1] + 0.5) * display_size

    # 3D
    center_x = location_x + offset_x - display_size / 2
    center_z = location_z + offset_y + size_scale * dimensions[0] / 2

    # 2D
    origin_x = center_x
    origin_y = center_z

    # 2D
    final_x = int(round((point[0] - origin_x) / size_scale))
    final_y = int(round((origin_y - point[2]) / size_scale))

    return (final_x, final_y)


def create_mesh(coordinates, name="MyObject", y_offset=0, angle_limit=None, dist=None):
    mesh = bpy.data.meshes.new("mesh")
    obj = bpy.data.objects.new(name, mesh)

    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    vertices = []

    for v in coordinates:
        v = v + (0, y_offset, 0)
        vert = bm.verts.new(v)
        vertices.append(vert)

    bm.faces.new(vertices)

    if dist is not None:
        bmesh.ops.dissolve_degenerate(bm, dist=dist, edges=bm.edges)
    if angle_limit is not None:
        bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(angle_limit), use_dissolve_boundaries=False,
                                 verts=bm.verts, edges=bm.edges, delimit={'NORMAL'})

    bm.to_mesh(mesh)
    bm.free()

    return obj


def create_vertices(coordinates, name="MyObject", y_offset=0, angle_limit=None, dist=None):
    mesh = bpy.data.meshes.new("mesh")
    obj = bpy.data.objects.new(name, mesh)

    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for v in coordinates:
        v = v + (0, y_offset, 0)
        bm.verts.new(v)

    if dist is not None:
        bmesh.ops.dissolve_degenerate(bm, dist=dist, edges=bm.edges)
    if angle_limit is not None:
        bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(angle_limit), use_dissolve_boundaries=False,
                                 verts=bm.verts, edges=bm.edges, delimit={'NORMAL'})

    bm.to_mesh(mesh)
    bm.free()

    return obj
