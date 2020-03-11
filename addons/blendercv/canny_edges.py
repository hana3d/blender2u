import bpy
import cv2
import bmesh
import numpy as np
from bpy_extras import view3d_utils
from .utils import convert_2d_to_3d, convert_3d_to_2d, create_mesh, create_vertices


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
    # dissolve_angle: bpy.props.FloatProperty(
    #     name="Dissolve Angle",
    #     description="Max angle for limited dissolve",
    #     default=5,
    #     min=0,
    #     max=180
    # )
    # merge_distance: bpy.props.FloatProperty(
    #     name="Merge Distance",
    #     description="Max distance to degenerate",
    #     default=0.01,
    #     min=0
    # )

    obj = None
    img = None
    tmp_obj = None
    pressed = False
    first_point = None
    second_point = None

    @staticmethod
    def create_tmp_mesh(obj, dimensions):
        coordinates = [
            convert_2d_to_3d(obj, dimensions, [0, 0]),
            convert_2d_to_3d(obj, dimensions, [0, dimensions[0]]),
            convert_2d_to_3d(obj, dimensions, [dimensions[1], dimensions[0]]),
            convert_2d_to_3d(obj, dimensions, [dimensions[1], 0])
        ]
        coordinates = np.array(coordinates)
        return create_mesh(coordinates, "tmp", 0.05)

    def cv_operation(self, context):
        first_point = convert_3d_to_2d(self.obj, self.img.shape, self.first_point)
        second_point = convert_3d_to_2d(self.obj, self.img.shape, self.second_point)

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, self.threshold_min, self.threshold_max,
                          self.aperture_size, L2gradient=True)
        for height_index, row in enumerate(edges[0:first_point[1]]):
            for width_index, pixel in enumerate(row):
                edges[height_index, width_index] = 0
        for height_index, row in enumerate(edges):
            for width_index, pixel in enumerate(row[0:first_point[0]]):
                edges[height_index, width_index] = 0
        for height_index, row in enumerate(edges[second_point[1]:]):
            for width_index, pixel in enumerate(row):
                edges[height_index + second_point[1], width_index] = 0
        for height_index, row in enumerate(edges):
            for width_index, pixel in enumerate(row[second_point[0]:]):
                edges[height_index, width_index + second_point[0]] = 0

        points = []
        for height_index, row in enumerate(edges):
            for width_index, pixel in enumerate(row):
                if pixel == 255:
                    points.append([width_index, height_index])

        coordinates = []
        for point in points:
            coordinates.append(convert_2d_to_3d(self.obj, self.img.shape, point))
        coordinates = np.array(coordinates)

        create_vertices(coordinates, "Edges", -0.01)

    def __init__(self):
        print("Init Canny")

    def __del__(self):
        print("Del Canny")

    def execute(self, context):
        print('EXECUTE')
        self.obj = bpy.context.active_object
        print('obj', self.obj)
        print('img', self.img)
        print('point1', self.first_point)
        print('point2', self.second_point)
        self.cv_operation(context)

        return {'FINISHED'}

    def modal(self, context, event):
        scene = context.scene
        region = context.region
        rv3d = context.space_data.region_3d
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            coord = (event.mouse_region_x, event.mouse_region_y)
            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
            ray_cast = scene.ray_cast(scene.view_layers[0], ray_origin, view_vector)
            if ray_cast[0] and ray_cast[4] == bpy.data.objects['tmp']:
                location = ray_cast[1]
                if self.pressed is False:
                    self.first_point = location
                    self.pressed = True
                else:
                    self.second_point = location
                    self.pressed = False
                    self.cv_operation(context)

                    bpy.ops.object.select_all(action='DESELECT')
                    self.tmp_obj.select_set(True)
                    bpy.ops.object.delete()
                    bpy.ops.object.select_all(action='DESELECT')
                    self.obj.select_set(True)
                    return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print('INVOKE')
        self.obj = bpy.context.active_object

        if self.obj.data.type != 'IMAGE':
            return {'FINISHED'}

        if hasattr(self.obj.data, 'filepath'):
            image_path = bpy.path.abspath(self.obj.data.filepath)
            self.img = cv2.imread(image_path, 1)

            self.tmp_obj = self.create_tmp_mesh(self.obj, self.img.shape)
            bpy.ops.object.select_all(action='DESELECT')
            self.obj.select_set(True)

            context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
