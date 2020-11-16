from bpy.types import Panel


class OBJECT_PT_ImportMaterialPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Import Material"
    bl_context = "objectmode"
    bl_category = "R2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('material.single_import', text='Import Material')
        row = layout.row()
        row.operator('material.multiple_import', text='Import Multiple Materials')
