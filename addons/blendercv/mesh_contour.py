import bpy
import cv2
import bmesh
import numpy as np
from .utils import find_contours, convert_coordinates, create_mesh


class MeshContourClass(bpy.types.Operator):
    """Mesh Contour Class"""
    bl_idname = "object.mesh_contour"
    bl_label = "Mesh Contour Class"
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

    def execute(self, context):
        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = bpy.path.abspath(obj.data.filepath)
            img = cv2.imread(image_path, 1)

            dimensions, cnt = find_contours(img)

            vertices = []
            for point in cnt:
                vertices.append(convert_coordinates(obj, dimensions, point))
            vertices = np.array(vertices)

            if self.resolution != 1:
                drop_ratio = int(round(1 / (1 - self.resolution)))
                vertices = np.delete(vertices, slice(None, None, drop_ratio), 0)

            create_mesh(vertices, self.dissolve_angle, self.merge_distance)

        return {'FINISHED'}
