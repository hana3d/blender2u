import bpy
import cv2
import bmesh
import numpy as np
from .utils import find_contours, convert_coordinates, create_mesh


class MeshContourProps(bpy.types.PropertyGroup):
    resolution: bpy.props.FloatProperty(
        name="Resolution",
        description="Number of vertices in the mesh",
        default=0.9,
        min=0,
        max=1
    )


class MeshContourClass(bpy.types.Operator):
    """Mesh Contour Class"""
    bl_idname = "object.mesh_contour"
    bl_label = "Mesh Contour Class"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        obj = bpy.context.active_object

        if hasattr(obj.data, 'filepath'):
            image_path = bpy.path.abspath(obj.data.filepath)
            img = cv2.imread(image_path, 1)

            dimensions, cnt = find_contours(img)

            vertices = []
            for point in cnt:
                vertices.append(convert_coordinates(obj, dimensions, point))
            vertices = np.array(vertices)

            resolution = scene.mesh_contour_props.resolution

            drop_total = (1 - resolution) * vertices.size
            drop_ratio = int(round(vertices.size / drop_total))

            vertices = np.delete(vertices, slice(None, None, drop_ratio), 0)

            create_mesh(vertices)

        return {'FINISHED'}
