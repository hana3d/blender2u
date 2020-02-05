import bpy
import cv2


class OpencvClass(bpy.types.Operator):
    """OpenCV Class"""
    bl_idname = "object.opencv_class"
    bl_label = "OpenCV Class"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = obj.data.filepath

            image = cv2.imread(image_path, 1)

            back_sub = cv2.createBackgroundSubtractorMOG2()

            fg_mask = back_sub.apply(image)

        return {'FINISHED'}
