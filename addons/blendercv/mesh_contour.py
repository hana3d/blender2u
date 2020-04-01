import bpy
import cv2
import bmesh
import numpy as np
from .utils import convert_2d_to_3d, create_mesh


class MeshContourClass(bpy.types.Operator):
    """Mesh Contour Class"""
    bl_idname = "object.mesh_contour"
    bl_label = "Mesh Contour"
    bl_options = {'REGISTER', 'UNDO'}

    resolution: bpy.props.FloatProperty(
        name="Resolution",
        description="Number of vertices in the mesh",
        default=0.9,
        min=0.34,
        max=1
    )

    dissolve_angle: bpy.props.FloatProperty(
        name="Dissolve Angle",
        description="Max angle for limited dissolve",
        default=5,
        min=0,
        max=180
    )

    merge_distance: bpy.props.FloatProperty(
        name="Merge Distance",
        description="Max distance to degenerate",
        default=0.01,
        min=0
    )

    @staticmethod
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

    def execute(self, context):
        bpy.ops.analytics.addons_analytics(self.bl_label)

        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = bpy.path.abspath(obj.data.filepath)
            img = cv2.imread(image_path, 1)

            dimensions, cnt = self.find_contours(img)

            vertices = []
            for point in cnt:
                vertices.append(convert_2d_to_3d(obj, dimensions, point[0]))
            vertices = np.array(vertices)

            if self.resolution != 1:
                drop_ratio = int(round(1 / (1 - self.resolution)))
                vertices = np.delete(vertices, slice(None, None, drop_ratio), 0)

            create_mesh(vertices, "Contour", -0.01, self.dissolve_angle, self.merge_distance)

        return {'FINISHED'}
