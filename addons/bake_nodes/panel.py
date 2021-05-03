import bpy
from bpy.types import Panel


class OBJECT_PT_NodesPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Bake Nodes'
    bl_context = 'objectmode'
    bl_category = 'R2U'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        layout = self.layout

        layout.template_list(
            'UI_UL_list',
            'nodes_panel',
            bpy.data,
            'materials',
            context.scene.bake_nodes,
            'selected_material_index',
            rows=3,
        )
        layout.prop(context.scene.bake_nodes, 'bake_diffuse')
        layout.prop(context.scene.bake_nodes, 'bake_metallic')
        layout.prop(context.scene.bake_nodes, 'bake_roughness')
        layout.prop(context.scene.bake_nodes, 'bake_normal')
        layout.operator('object.bake_nodes', text='Bake Nodes', icon='MOD_BOOLEAN')
