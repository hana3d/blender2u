import bpy
from bpy.types import Panel
from . import addon_updater_ops


@addon_updater_ops.make_annotations
class Blender2UPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        # layout = self.layout
        # col = layout.column() # works best if a column, or even just self.layout
        # mainrow = layout.row()
        # col = mainrow.column()

        # updater draw function
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # col.operator("wm.url_open","Open webpage ").url=addon_updater_ops.updater.website


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

        mainrow = layout.row()
        col = mainrow.column()
        addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Call to check for update in background
        # note: built-in checks ensure it runs at most once
        # and will run in the background thread, not blocking
        # or hanging blender
        # Internally also checks to see if auto-check enabled
        # and if the time interval has passed
        addon_updater_ops.check_for_update_background()

        # could also use your own custom drawing
        # based on shared variables
        # if addon_updater_ops.updater.update_ready is True:
        #     layout.label(text="Custom update message", icon="INFO")
        # layout.label(text="")

        # call built-in function with draw code/checks
        addon_updater_ops.update_notice_box_ui(self, context)

        # row = layout.row()
        # row.operator('object.glb_usdz_export', text='GLB USDZ Export', icon='MOD_BOOLEAN')
