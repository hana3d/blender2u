import bpy
import bgl
import gpu
import cv2
import numpy as np
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils
from mathutils import Vector
from .utils import convert_2d_to_3d, convert_3d_to_2d, create_mesh, create_vertices


def draw(self, context, mouse_start, mouse_end):
    vertices = (
        self.mouse_start, (self.mouse_end[0], self.mouse_start[1]),
        (self.mouse_start[0], self.mouse_end[1]), self.mouse_end)

    indices = ((0, 1, 2), (2, 1, 3))

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", (0.6, 0.8, 0.8, 0.5))
    bgl.glEnable(bgl.GL_BLEND)
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)


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

    obj = bpy.types.Object
    img = np.ndarray
    tmp_obj = bpy.types.Object
    pressed = False
    first_point = Vector
    second_point = Vector
    mouse_start = (int, int)
    mouse_end = (int, int)
    # _handle = bpy.types.Object

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

        if first_point[0] < second_point[0]:
            min_x = first_point[0]
            max_x = second_point[0]
        else:
            min_x = second_point[0]
            max_x = first_point[0]

        if first_point[1] < second_point[1]:
            min_y = first_point[1]
            max_y = second_point[1]
        else:
            min_y = second_point[1]
            max_y = first_point[1]

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, self.threshold_min, self.threshold_max,
                          self.aperture_size, L2gradient=True)
        for height_index, row in enumerate(edges[0:min_y]):
            for width_index, pixel in enumerate(row):
                edges[height_index, width_index] = 0
        for height_index, row in enumerate(edges):
            for width_index, pixel in enumerate(row[0:min_x]):
                edges[height_index, width_index] = 0
        for height_index, row in enumerate(edges[max_y:]):
            for width_index, pixel in enumerate(row):
                edges[height_index + max_y, width_index] = 0
        for height_index, row in enumerate(edges):
            for width_index, pixel in enumerate(row[max_x:]):
                edges[height_index, width_index + max_x] = 0

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
                    self.mouse_start = (event.mouse_region_x, event.mouse_region_y)
                    self.mouse_end = (event.mouse_region_x, event.mouse_region_y)
                    self.pressed = True
                    args = (self, context, self.mouse_start, self.mouse_end)
                    self._handle = bpy.types.SpaceView3D.draw_handler_add(draw, args, 'WINDOW', 'POST_PIXEL')
                else:
                    self.second_point = location
                    self.pressed = False
                    bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                    self.cv_operation(context)

                    bpy.ops.object.select_all(action='DESELECT')
                    self.tmp_obj.select_set(True)
                    bpy.ops.object.delete()
                    bpy.ops.object.select_all(action='DESELECT')
                    self.obj.select_set(True)
                    return {'FINISHED'}
        elif event.type == 'MOUSEMOVE' and self.pressed is True:
            self.mouse_end = (event.mouse_region_x, event.mouse_region_y)
            context.area.tag_redraw()
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

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
