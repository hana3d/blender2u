import bpy
from bpy.types import Panel


class OBJECT_PT_CollectionGridPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Collection Grid"
    bl_context = "objectmode"
    bl_category = "R2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        scene = context.scene
        layout = self.layout

        layout.prop(scene.collection_grid_props, "rows")
        layout.prop(scene.collection_grid_props, "distance")
        layout.prop(scene.collection_grid_props, "switch")

        row = layout.row()
        row.operator('object.collection_grid', text='Create Scene Grid', icon='MOD_BOOLEAN')
