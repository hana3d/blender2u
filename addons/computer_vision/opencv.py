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

            img = cv2.imread(image_path, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

            # (2) Morph-op to remove noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

            # (3) Find the max-area contour
            cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            cnt = sorted(cnts, key=cv2.contourArea)[-1]

            print(cnt)

        return {'FINISHED'}
