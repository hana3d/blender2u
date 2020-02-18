import bpy
import bmesh
import cv2
import math


def find_contours(img):
    blur = cv2.bilateralFilter(img, 9, 75, 75)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, kernel)

    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    dimensions = img.shape

    return dimensions, cnt


def convert_coordinates(obj, dimensions, cnt):
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
    contour_x = cnt[0][0] * size_scale
    contour_y = cnt[0][1] * size_scale

    # 3D
    final_x = center_x + contour_x
    final_y = center_y
    final_z = center_z - contour_y

    return (final_x, final_y, final_z)


def create_mesh(coordinates, angle_limit, dist):
    mesh = bpy.data.meshes.new("mesh")
    obj = bpy.data.objects.new("MyObject", mesh)

    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    vertices = []

    for v in coordinates:
        vert = bm.verts.new(v)
        vertices.append(vert)

    bm.faces.new(vertices)

    bmesh.ops.dissolve_degenerate(bm, dist=dist, edges=bm.edges)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(angle_limit), use_dissolve_boundaries=False,
                             verts=bm.verts, edges=bm.edges, delimit={'NORMAL'})

    bm.to_mesh(mesh)
    bm.free()
