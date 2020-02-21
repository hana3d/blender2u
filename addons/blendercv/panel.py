import bpy
from bpy.types import Panel


class OBJECT_PT_ContourPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Find Contours"
    bl_context = "objectmode"
    bl_category = "BlenderCV"

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('object.mesh_contour', text='Mesh Contour', icon='MOD_BOOLEAN')


class OBJECT_PT_CannyPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Canny Edges"
    bl_context = "objectmode"
    bl_category = "BlenderCV"

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('object.canny_edges', text='Canny Edges', icon='MOD_BOOLEAN')
