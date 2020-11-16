import bpy
from bpy.types import Panel


class OBJECT_PT_UVPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "UV Check"
    bl_context = "objectmode"
    bl_category = "R2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('object.uv_apply', text='Apply Checker Texture', icon='MOD_BOOLEAN')
        row = layout.row()
        row.operator('object.uv_remove', text='Remove Checker Texture', icon='MOD_BOOLEAN')
