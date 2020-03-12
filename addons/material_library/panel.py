import bpy
from bpy.types import Panel


class MATLIB_PT_MatLibPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Material Library VX"
    bl_context = "objectmode"
    bl_category = "MatLib"

    # @classmethod
    # def poll(self, context):
    #     return context.active_object.active_material is not None

    def draw(self, context):
        layout = self.layout
        matlib = context.scene.matlib

        # libraries
        col = layout.column(align=True)
        if matlib.current_library:
            text = matlib.current_library.shortname
        else:
            text = "Select a Library"

        row = layout.row()
        row.menu("MATLIB_MT_LibsMenu", text=text)
        row = layout.row()
        row.operator("matlib.operator", icon="ADD",
                     text="New Library").cmd = "LIBRARY_ADD"

        # list
        row = layout.row()
        row.template_list("UI_UL_list", "  ", matlib,
                          "materials", matlib, "mat_index", rows=6)
        row = layout.row()
        col = row.column()

        # operators
        col.operator("matlib.operator", icon="ADD",
                     text="Add To Library").cmd = "ADD"
        col.operator("matlib.operator", icon="MATERIAL",
                     text="Apply To Selected").cmd = "APPLY"
        col.operator("matlib.operator", icon="FILE_REFRESH",
                     text="Reload Material").cmd = "RELOAD"
        col.operator("matlib.operator", icon="COLOR",
                     text="Preview Material").cmd = "PREVIEW"
        col.operator("matlib.operator", icon="GHOST_DISABLED",
                     text="Remove Preview").cmd = "FLUSH"
        col.operator("matlib.operator", icon="REMOVE",
                     text="Remove Material").cmd = "REMOVE"
        col.prop(matlib, "show_prefs", icon="MODIFIER", text="Settings")

        # Search
        if not matlib.hide_search:
            row = layout.row(align=True)
            row.prop_search(matlib, "search", matlib,
                            "materials", text="", icon="VIEWZOOM")

        # categories
        row = layout.row()
        if matlib.active_material:
            row.label(text="Category:")
            row.label(text=matlib.active_material.category)
        else:
            row.label(text="Category Tools:")
        row = layout.row(align=True)
        text = "All"
        if matlib.current_category:
            text = matlib.current_category
        row.menu("MATLIB_MT_CatsMenu", text=text)
        row = layout.row(align=True)
        row.prop(matlib, "filter", icon="FILTER", text="Filter")
        row.operator("matlib.operator", icon="FILE_PARENT",
                     text="Set Type").cmd = "FILTER_SET"
        row.operator("matlib.operator", icon="ADD",
                     text="New").cmd = "FILTER_ADD"
        row.operator("matlib.operator", icon="REMOVE",
                     text="Remove").cmd = "FILTER_REMOVE"

        # prefs
        if matlib.show_prefs:
            row = layout.row(align=True)
            row.prop(matlib, "force_import")
            row.prop(matlib, "link")
            row.prop(matlib, "hide_search")

        if matlib.active_material is not None:
            col = layout.box().column()
            col.template_preview(bpy.data.materials[matlib.active_material.name])
