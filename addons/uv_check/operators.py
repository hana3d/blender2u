import os
from typing import List

import bpy

MATERIAL_NAME = '.UVMT'
TEXTURE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UV_CHECK.png')


def create_material(context: bpy.types.Context, material_name: str):
    mat = bpy.data.materials.new(material_name)
    mat.use_nodes = True
    node_tree = mat.node_tree

    image_node = node_tree.nodes.new(type='ShaderNodeTexImage')
    image_node.image = bpy.data.images.load(TEXTURE_PATH)
    node_tree.links.new(image_node.outputs['Color'],
                        node_tree.nodes['Principled BSDF'].inputs['Base Color'])


def apply_textures(objects: List[bpy.types.Object], material_name: str):
    for obj in objects:
        if obj.type != 'MESH':
            continue
        if obj.active_material is None:
            obj.original_material.add().add_material(None)
        elif material_name not in obj.active_material.name:
            obj.original_material.clear()
            if (len(obj.material_slots) > 1):
                for index, material_slot in enumerate(obj.material_slots):
                    original_material = obj.original_material.add()
                    original_material.add_material(material_slot.material)
                    for face in obj.data.polygons:
                        if (face.material_index == index):
                            original_material.add_face(face.index)
            else:
                obj.original_material.add().add_material(obj.material_slots[0].material)
            obj.data.materials.clear()
        else:
            obj.data.materials.clear()

        obj.active_material = bpy.data.materials[material_name]


class ApplyUVTextureAll(bpy.types.Operator):
    """Apply Checker Texture"""
    bl_idname = "object.uv_apply_all"
    bl_label = "UV Check"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.data.materials.get(MATERIAL_NAME) is None:
            create_material(context, MATERIAL_NAME)

        apply_textures(context.scene.objects, MATERIAL_NAME)

        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except Exception as error:
            print(error)
            print('Addon analytics not installed')

        return self.execute(context)


class ApplyUVTextureSelected(bpy.types.Operator):
    """Apply Checker Texture"""
    bl_idname = "object.uv_apply_selected"
    bl_label = "UV Check"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.data.materials.get(MATERIAL_NAME) is None:
            create_material(context, MATERIAL_NAME)

        apply_textures(context.selected_objects, MATERIAL_NAME)

        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except Exception as error:
            print(error)
            print('Addon analytics not installed')

        return self.execute(context)


class RemoveUVTexture(bpy.types.Operator):
    """Remove Checker Texture"""
    bl_idname = "object.uv_remove"
    bl_label = "Remove Checker Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.type != 'MESH':
                continue
            if len(obj.original_material) > 0:
                if obj.original_material[0].material != obj.active_material:
                    obj.data.materials.clear()
                    if len(obj.original_material) > 1:
                        for index, material_slots in enumerate(obj.original_material):
                            obj.data.materials.append(material_slots.material)
                            for face in material_slots.faces:
                                print('Face', face.face)
                                print('Index', index)
                                obj.data.polygons[face.face].material_index = index
                    else:
                        obj.data.materials.append(obj.original_material[0].material)

        return {'FINISHED'}
