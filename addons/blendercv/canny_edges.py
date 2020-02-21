import bpy
import cv2
import bmesh
# from .utils import find_contours, convert_coordinates, create_mesh


class CannyEdgesClass(bpy.types.Operator):
    """Canny Edges Class"""
    bl_idname = "object.canny_edges"
    bl_label = "Canny Edges Class"
    bl_options = {'REGISTER', 'UNDO'}

    threshold_max: bpy.props.FloatProperty(
        name="Max Threshold",
        description="Max Threshold",
        default=200
    )

    threshold_min: bpy.props.FloatProperty(
        name="Min Threshold",
        description="Min Threshold",
        default=100
    )

    aperture_size: bpy.props.IntProperty(
        name="Aperture Size",
        description="Aperture Size",
        default=3
    )

    def execute(self, context):
        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = bpy.path.abspath(obj.data.filepath)
            img = cv2.imread(image_path, 1)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, self.threshold_min, self.threshold_max,
                              self.aperture_size, L2gradient=True)

            print(edges)

        return {'FINISHED'}
