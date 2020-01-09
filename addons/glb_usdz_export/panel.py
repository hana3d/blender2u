import bpy
from bpy.types import Panel


class GLBUSDZPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "GLB USDZ Export"
    bl_context = "objectmode"
    bl_category = "Real2U"

    def draw(self, context):
        global custom_icons

        layout = self.layout

        # Bool diff button
        row = layout.row()
        row.operator('object.glb_usdz_export', text='Export Scene', icon='MOD_BOOLEAN')
