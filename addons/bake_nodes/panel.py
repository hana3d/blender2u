import bpy
from bpy.types import Panel


class NodesPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Bake Nodes"
    bl_context = "objectmode"
    bl_category = "Real2U"

    def draw(self, context):
        global custom_icons

        layout = self.layout

        # Bool diff button
        row = layout.row()
        row.operator('object.bake_nodes', text='Bake Nodes', icon='MOD_BOOLEAN')
