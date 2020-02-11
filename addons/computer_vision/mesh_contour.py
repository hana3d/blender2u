import bpy
import cv2
import bmesh
from .utils import find_contours, convert_coordinates, create_mesh


class MeshContourClass(bpy.types.Operator):
    """Mesh Contour Class"""
    bl_idname = "object.mesh_contour"
    bl_label = "Mesh Contour Class"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = bpy.path.abspath(obj.data.filepath)
            img = cv2.imread(image_path, 1)

            dimensions, cnt = find_contours(img)

            vertices = []
            for point in cnt:
                vertices.append(convert_coordinates(obj, dimensions, point))

            create_mesh(vertices)

        return {'FINISHED'}
