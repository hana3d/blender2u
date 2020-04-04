import bpy
from math import sqrt, ceil
from .utils import get_material


def add_material_spheres(context, matlib):
    scene = context.scene

    for mat in matlib.materials:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, enter_editmode=False, location=(0, 0, 0))
        get_material(mat.name)
        context.active_object.name = mat.name
        context.active_object.active_material = bpy.data.materials[mat.name]

    scene.collection_grid_props.rows = ceil(sqrt(len(matlib.materials)))
    scene.collection_grid_props.distance = 1.0
    scene.collection_grid_props.switch = True
    bpy.ops.object.collection_grid()


class CreateScene(bpy.types.Operator):
    """Create Matlib Scene"""
    bl_idname = "matlib.create_scene"
    bl_label = "Create Matlib Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        matlib = context.scene.matlib

        bpy.ops.scene.new(type='EMPTY')
        context.scene.name = "MatLib"

        add_material_spheres(context, matlib)

        context.space_data.shading.type = 'MATERIAL'

        return {'FINISHED'}
