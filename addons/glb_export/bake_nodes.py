import bpy


def bake_nodes(obj):
    if hasattr(obj.active_material, 'node_tree'):
        if len(obj.active_material.node_tree.nodes) > 2:
            node_tree = obj.active_material.node_tree

            node = node_tree.nodes.new("ShaderNodeTexImage")
            node.select = True
            node_tree.nodes.active = node
            newimg = bpy.data.images.new('bakeImg', 1024, 1024)
            node.image = newimg

            bpy.ops.object.bake(type='COMBINED')

            node_tree.links.new(node_tree.nodes["Image Texture"].outputs[0], node_tree.nodes["Principled BSDF"].inputs[0])
            bpy.ops.object.select_all(action='DESELECT')
