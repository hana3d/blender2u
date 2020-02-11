import bpy
from bpy.types import Panel


class OBJECT_PT_CVPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Computer Vision"
    bl_context = "objectmode"
    bl_category = "Real2U"

    def draw(self, context):
        global custom_icons

        scene = context.scene
        layout = self.layout

        # Bool diff button
        row = layout.row()
        row.operator('object.mesh_contour', text='Mesh Contour', icon='MOD_BOOLEAN')

        layout.prop(scene.mesh_contour_props, "resolution")

        row = layout.row()
        row.operator('object.canny_edges', text='Canny Edges', icon='MOD_BOOLEAN')
