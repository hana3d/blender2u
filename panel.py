import bpy
from . import addon_updater_ops
from bpy.types import Panel


class OBJECT_PT_Blender2UPanel(Panel):
    """Panel to demo popup notice and ignoring functionality"""
    bl_label = "Blender2U"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "Real2U"

    def draw(self, context):
        layout = self.layout

        # Call to check for update in background
        # note: built-in checks ensure it runs at most once
        # and will run in the background thread, not blocking
        # or hanging blender
        # Internally also checks to see if auto-check enabled
        # and if the time interval has passed
        addon_updater_ops.check_for_update_background()

        # could also use your own custom drawing
        # based on shared variables
        if addon_updater_ops.updater.update_ready is True:
            layout.label(text="Custom update message", icon="INFO")
        layout.label(text="")

        # call built-in function with draw code/checks
        addon_updater_ops.update_notice_box_ui(self, context)

        row = layout.row()
        row.operator('object.glb_usdz_export', text='GLB USDZ Export', icon='MOD_BOOLEAN')
