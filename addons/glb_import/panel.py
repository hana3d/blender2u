import bpy
from bpy.types import Panel


class OBJECT_PT_GLBImportPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "GLB Import"
    bl_context = "objectmode"
    bl_category = "R2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('import_scene.glb_import', text='Import Files', icon='MOD_BOOLEAN')
