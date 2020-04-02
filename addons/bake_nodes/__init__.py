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
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 4, 0),
    "location": "",
    "warning": "",
    "category": "Material"
}

# import os
import bpy
from .panel import OBJECT_PT_NodesPanel


def bake_object(mat, bakeType, inputNode):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_plane_add(location=(789, 789, 789))
    plane = bpy.context.active_object
    plane.active_material = mat

    plane.select_set(True)
    node_tree = plane.active_material.node_tree

    node = node_tree.nodes.new("ShaderNodeTexImage")
    node.select = True
    node_tree.nodes.active = node
    newimg = bpy.data.images.new(bakeType, 2048, 2048)
    node.image = newimg

    bpy.ops.object.bake(type=bakeType)

    node_tree.links.new(node.outputs[0], node_tree.nodes["Principled BSDF"].inputs[inputNode])
    bpy.ops.object.delete(use_global=True, confirm=False)
    bpy.ops.object.select_all(action='DESELECT')


class BakeNodes(bpy.types.Operator):
    """Bake Nodes"""
    bl_idname = "object.bake_nodes"
    bl_label = "Bake Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)

        # if os.path.exists(bpy.utils.resource_path('USER').replace(' ', '') + os.sep + 'scripts' + os.sep + 'addons'
        #                   + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'bake_nodes' + os.sep + 'lightroom_14b.hdr'):
        #     hdr_path = bpy.utils.resource_path('USER').replace(' ', '') + os.sep + 'scripts' + os.sep + 'addons' \
        #         + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'bake_nodes' + os.sep + 'lightroom_14b.hdr'
        # elif os.path.exists(bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons'
        #                     + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'bake_nodes' + os.sep + 'lightroom_14b.hdr'):
        #     hdr_path = bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' \
        #         + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'bake_nodes' + os.sep + 'lightroom_14b.hdr'
        # else:
        #     self.report({'ERROR'}, "hdr path not found")
        #     return {'CANCELLED'}

        # world = context.scene.world
        # world.use_nodes = True
        # nt = context.scene.world.node_tree
        # enode = nt.nodes.new("ShaderNodeTexEnvironment")
        # # enode.image = bpy.data.images.load(hdr_path)

        # backNode = nt.nodes['Background']
        # gradColOut = enode.outputs['Color']
        # backColIn = backNode.inputs['Color']
        # nt.links.new(gradColOut, backColIn)

        context.scene.render.engine = 'CYCLES'

        for mat in bpy.data.materials:
            if hasattr(mat, 'node_tree'):
                if len(mat.node_tree.nodes) > 2:
                    if mat.node_tree.nodes["Principled BSDF"].inputs[0].is_linked:
                        context.scene.render.bake.use_pass_direct = False
                        context.scene.render.bake.use_pass_indirect = False
                        context.scene.render.bake.use_pass_color = True
                        bake_object(mat, 'DIFFUSE', 0)

                    if mat.node_tree.nodes["Principled BSDF"].inputs[19].is_linked:
                        bake_object(mat, 'NORMAL', 19)

                    if mat.node_tree.nodes["Principled BSDF"].inputs[7].is_linked:
                        bake_object(mat, 'ROUGHNESS', 7)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(BakeNodes.bl_idname)


def register():
    bpy.utils.register_class(BakeNodes)
    bpy.utils.register_class(OBJECT_PT_NodesPanel)
    # bpy.types.TOPBAR_MT_edit.append(menu_func)


def unregister():
    # bpy.types.TOPBAR_MT_edit.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_PT_NodesPanel)
    bpy.utils.unregister_class(BakeNodes)


if __name__ == "__main__":
    register()
