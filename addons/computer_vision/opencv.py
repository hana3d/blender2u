import bpy
import cv2
import bmesh


def find_contours(image_path):
    img = cv2.imread(image_path, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

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

    # print(size_scale)
    # print(center_x, center_y, center_z)
    # print('Height: ', dimensions[0])
    # print('Width: ', dimensions[1])
    # print('First Point: ', cnt[0][0])


def create_mesh(coordinates):
    mesh = bpy.data.meshes.new("mesh")
    obj = bpy.data.objects.new("MyObject", mesh)

    scene = bpy.context.scene
    scene.collection.objects.link(obj)  # put the object into the scene (link)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene
    obj.select_set(True)  # select object

    mesh = bpy.context.object.data
    bm = bmesh.new()

    vertices = []

    for v in coordinates:
        vert = bm.verts.new(v)  # add a new vert
        vertices.append(vert)

    bm.faces.new(vertices)

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()


class OpencvClass(bpy.types.Operator):
    """OpenCV Class"""
    bl_idname = "object.opencv_class"
    bl_label = "OpenCV Class"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = bpy.path.abspath(obj.data.filepath)

            dimensions, cnt = find_contours(image_path)

            vertices = []
            for point in cnt:
                vertices.append(convert_coordinates(obj, dimensions, point))

            create_mesh(vertices)

        return {'FINISHED'}
