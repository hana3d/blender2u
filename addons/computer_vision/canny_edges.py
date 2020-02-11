import bpy
import cv2
import bmesh
# from .utils import find_contours, convert_coordinates, create_mesh


class CannyEdgesClass(bpy.types.Operator):
    """Canny Edges Class"""
    bl_idname = "object.canny_edges"
    bl_label = "Canny Edges Class"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = bpy.path.abspath(obj.data.filepath)
            img = cv2.imread(image_path, 1)

            edges = cv2.Canny(img, 100, 200)

            print(edges)

        return {'FINISHED'}
