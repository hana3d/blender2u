from bpy.types import Panel


class OBJECT_PT_NodesIOPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Nodes IO"
    bl_context = "objectmode"
    bl_category = "Real2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('node.import_nodes', text='Import from YAML')
        row = layout.row()
        row.operator('node.export_nodes', text='Export to YAML')
