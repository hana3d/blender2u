import bpy
from bpy.types import Panel


class AutoScalePanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Auto Scale"
    bl_context = "objectmode"
    bl_category = "Real2U"

    def draw(self, context):
        global custom_icons

        layout = self.layout

        # Bool diff button
        row = layout.row()
        row.operator('object.auto_scale', text='Scale Selected Objects', icon='MOD_BOOLEAN')

        row = layout.row()
        row.operator('object.csv_scale', text='Choose CSV File', icon='MOD_BOOLEAN')
