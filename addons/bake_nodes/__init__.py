# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "bake-nodes",
    "author": "R2U",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 4, 2),
    "location": "",
    "warning": "",
    "category": "Material"
}

from contextlib import suppress

import bpy

from .panel import OBJECT_PT_NodesPanel


class BakeNodesProps(bpy.types.PropertyGroup):
    selected_material_index: bpy.props.IntProperty(
        name='Material to bake',
        description='Index of material to bake',
        default=0,
    )

    bake_diffuse: bpy.props.BoolProperty(
        name='Base Color',
        description='Bake nodes connected to Base Color input',
        default=False,
    )

    bake_metallic: bpy.props.BoolProperty(
        name='Mettalic',
        description='Bake nodes connected to Mettalic input',
        default=False,
    )

    bake_roughness: bpy.props.BoolProperty(
        name='Roughness',
        description='Bake nodes connected to Roughness input',
        default=False,
    )

    bake_normal: bpy.props.BoolProperty(
        name='Normal',
        description='Bake nodes connected to Normal Map',
        default=False,
    )


def bake_nodes(mat: bpy.types.Material, bake_type: str, input_socket: int, color_space: str):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_plane_add(location=(789, 789, 789))
    plane = bpy.context.active_object
    plane.active_material = mat

    plane.select_set(True)
    node_tree = plane.active_material.node_tree

    emission_node = node_tree.nodes.new('ShaderNodeEmission')
    emission_node.inputs[1].default_value = 1

    if bake_type == 'NORMAL':
        src_node = node_tree.nodes['Normal Map']
    else:
        src_node = node_tree.nodes['Principled BSDF']

    for link in node_tree.links:
        if (
            link.to_node == src_node
            and link.to_socket == src_node.inputs[input_socket]
        ):
            output_socket = link.from_socket
    node_tree.links.new(
        emission_node.outputs[0],
        node_tree.nodes['Material Output'].inputs[0]
    )
    node_tree.links.new(
        output_socket,
        emission_node.inputs[0]
    )

    node = node_tree.nodes.new('ShaderNodeTexImage')
    node.select = True
    node_tree.nodes.active = node
    new_img = bpy.data.images.new(f'{mat.name}_{bake_type}', 1024, 1024)
    new_img.colorspace_settings.name = color_space
    new_img.use_fake_user = True
    node.image = new_img

    bpy.ops.object.bake(type='EMIT', save_mode='EXTERNAL')

    node_tree.links.new(node.outputs[0], src_node.inputs[input_socket])

    node_tree.links.new(
        node_tree.nodes['Principled BSDF'].outputs[0],
        node_tree.nodes['Material Output'].inputs[0]
    )

    node_tree.nodes.remove(emission_node)

    bpy.ops.object.delete(use_global=True, confirm=False)
    bpy.ops.object.select_all(action='DESELECT')


class BakeNodes(bpy.types.Operator):
    """Bake Nodes"""
    bl_idname = 'object.bake_nodes'
    bl_label = 'Bake Nodes'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.render.engine = 'CYCLES'
        context.scene.cycles.device = 'CPU'
        context.scene.cycles.bake_type = 'EMIT'
        context.scene.cycles.samples = 32

        mat = bpy.data.materials[context.scene.bake_nodes.selected_material_index]

        with suppress(AttributeError):
            if context.scene.bake_nodes.bake_diffuse:
                context.scene.render.bake.use_pass_direct = False
                context.scene.render.bake.use_pass_indirect = False
                context.scene.render.bake.use_pass_color = True
                context.scene.sequencer_colorspace_settings.name = 'sRGB'
                bake_nodes(mat, 'DIFFUSE', 0, 'sRGB')

            if context.scene.bake_nodes.bake_metallic:
                context.scene.sequencer_colorspace_settings.name = 'Non-Color'
                bake_nodes(mat, 'METALLIC', 4, 'Non-Color')

            if context.scene.bake_nodes.bake_roughness:
                context.scene.sequencer_colorspace_settings.name = 'Non-Color'
                bake_nodes(mat, 'ROUGHNESS', 7, 'Non-Color')

            if context.scene.bake_nodes.bake_normal:
                context.scene.sequencer_colorspace_settings.name = 'Non-Color'
                bake_nodes(mat, 'NORMAL', 1, 'Non-Color')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(BakeNodesProps)
    bpy.utils.register_class(BakeNodes)
    bpy.utils.register_class(OBJECT_PT_NodesPanel)
    bpy.types.Scene.bake_nodes = bpy.props.PointerProperty(type=BakeNodesProps)


def unregister():
    del bpy.types.Scene.bake_nodes
    bpy.utils.unregister_class(OBJECT_PT_NodesPanel)
    bpy.utils.unregister_class(BakeNodes)
    bpy.utils.unregister_class(BakeNodesProps)


if __name__ == '__main__':
    register()
