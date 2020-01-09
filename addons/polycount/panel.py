import bpy
from bpy.types import Panel


class PolycountPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Polycount"
    bl_context = "objectmode"
    bl_category = "Real2U"

    def draw(self, context):
        global custom_icons

        layout = self.layout

        # Bool diff button
        row = layout.row()
        row.operator('object.polycount_collections', text='Count Collections', icon='MOD_BOOLEAN')
        row = layout.row()
        row.operator('object.polycount_objects', text='Count Objects', icon='MOD_BOOLEAN')
        row = layout.row()
        row.operator('object.color_objects', text='Heatmap', icon='MOD_BOOLEAN')
        row = layout.row()
        row.operator('object.original_color', text='Remove Heatmap', icon='MOD_BOOLEAN')
