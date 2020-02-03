import bpy
import cv2


class OpencvClass(bpy.types.Operator):
    """OpenCV Class"""
    bl_idname = "object.opencv_class"
    bl_label = "OpenCV Class"
    bl_options = {'REGISTER', 'UNDO'}
