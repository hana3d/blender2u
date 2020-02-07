import bpy


class SubstancePanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Substance Integration"
    bl_context = "objectmode"
    bl_category = "Real2U"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        hh_settings = scene.hh_settings

        lbl = "Start listening"
        if hh_settings.active:
            lbl = "Stop listening"
        layout.operator("wm.hhconnect_timer_operator", text=lbl)
        layout.prop(hh_settings, "time")
        layout.operator("hhops.del_mats", text="Del Unused Mats")
        layout.operator("hhops.del_txts", text="Del Unused Txts")
        layout.operator("hhops.del_all", text="Del Unused")
