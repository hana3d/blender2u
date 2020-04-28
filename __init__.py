bl_info = {
    "name": "Blender2U",
    "author": "Real2U",
    "description": "Add-ons developed by Real2U",
    "blender": (2, 80, 0),
    "version": (1, 6, 0),
    "location": "",
    "warning": "",
    "wiki_url": "https://gitlab.com/real2u/blender2u",
    "category": "System"
}

import bpy
from . import addon_updater_ops, ui
from .addons import analytics, auto_scale, bake_nodes, \
    collection_grid, glb_export, polycount, uv_check, \
    hh_connect, blendercv, mesh_lint, material_library


classes = (
    ui.Blender2UPreferences,
    ui.OBJECT_PT_Blender2UPanel
)

addons = {
    analytics,
    auto_scale,
    bake_nodes,
    collection_grid,
    glb_export,
    polycount,
    uv_check,
    blendercv,
    mesh_lint,
    material_library,
    hh_connect
}


def register():
    addon_updater_ops.register(bl_info)

    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)

    for addon in addons:
        addon.register()


def unregister():
    addon_updater_ops.unregister()

    for addon in addons:
        addon.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
