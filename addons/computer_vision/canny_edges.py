import bpy
import cv2
import bmesh
from .utils import find_contours, convert_coordinates, create_mesh


class CannyEdgesClass(bpy.types.Operator):
    """Canny Edges Class"""
    bl_idname = "object.canny_edges"
    bl_label = "Canny Edges Class"
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
