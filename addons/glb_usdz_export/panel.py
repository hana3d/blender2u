import bpy
from bpy.types import Panel


class OBJECT_PT_GLBUSDZPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "GLB USDZ Export"
    bl_context = "objectmode"
    bl_category = "Real2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('object.glb_usdz_export', text='Export Scene', icon='MOD_BOOLEAN')
