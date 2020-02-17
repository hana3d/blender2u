import operator
import bpy


class ApplyUVTexture(bpy.types.Operator):
    """Apply Checker Texture"""
    bl_idname = "object.uv_apply"
    bl_label = "Apply Checker Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.data.materials.get('.UVMT') is None:
            mat = bpy.data.materials.new(".UVMT")
            mat.use_nodes = True
            node_tree = mat.node_tree

            nodeTexChecher = node_tree.nodes.new("ShaderNodeTexChecker")
            node_tree.links.new(nodeTexChecher.outputs[0], node_tree.nodes["Principled BSDF"].inputs[0])
            nodeMapping = node_tree.nodes.new("ShaderNodeMapping")
            node_tree.links.new(nodeMapping.outputs[0], nodeTexChecher.inputs[0])
            nodeTexCoord = node_tree.nodes.new("ShaderNodeTexCoord")
            node_tree.links.new(nodeTexCoord.outputs[2], nodeMapping.inputs[0])

        for obj in bpy.context.scene.objects:
            if obj.active_material is None:
                obj.original_material.add().add(None)
            elif ".UVMT" not in obj.active_material.name:
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

            obj.active_material = bpy.data.materials['.UVMT']

        return {'FINISHED'}


class RemoveUVTexture(bpy.types.Operator):
    """Remove Checker Texture"""
    bl_idname = "object.uv_remove"
    bl_label = "Remove Checker Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
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
