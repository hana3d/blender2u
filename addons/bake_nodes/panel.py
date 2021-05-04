import bpy


class OBJECT_PT_NodesPanel(bpy.types.Panel):
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
            context.active_object,
            'material_slots',
            context.scene.bake_nodes,
            'selected_material_index',
            rows=3,
        )
        layout.prop(context.scene.bake_nodes, 'bake_diffuse')
        layout.prop(context.scene.bake_nodes, 'bake_metallic')
        layout.prop(context.scene.bake_nodes, 'bake_roughness')
        layout.prop(context.scene.bake_nodes, 'bake_normal')
        layout.prop(context.scene.bake_nodes, 'resolution')
        layout.operator('object.bake_nodes', text='Bake Nodes', icon='MOD_BOOLEAN')
