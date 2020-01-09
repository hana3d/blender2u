import bpy
from bpy.types import Panel


class USDZExporterPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "USDZ Export"
    bl_context = "objectmode"
    bl_category = "Real2U"

    def draw(self, context):
        global custom_icons

        layout = self.layout

        # Bool diff button
        row = layout.row()
        row.operator('object.usdz_export', text='Choose Folder', icon='MOD_BOOLEAN')
