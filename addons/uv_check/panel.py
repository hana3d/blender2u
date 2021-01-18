from bpy.types import Panel


class OBJECT_PT_UVPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "UV Check"
    bl_context = "objectmode"
    bl_category = "R2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('object.uv_apply_all', text='Apply To All Objects')
        row = layout.row()
        row.operator('object.uv_apply_selected', text='Apply Only To Selected Objects')
        row = layout.row()
        row.operator('object.uv_remove', text='Remove Checker Texture', icon='REMOVE')
