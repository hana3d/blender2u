bl_info = {
    "name": "Blender2U",
    "author": "R2U",
    "description": "Add-ons developed by R2U",
    "blender": (2, 92, 0),
    "version": (1, 9, 7),
    "location": "",
    "warning": "",
    "wiki_url": "https://github.com/hana3d/blender2u",
    "category": "System"
}

import bpy

from . import addon_updater_ops, ui
from .addons import (
    auto_scale,
    bake_nodes,
    collection_grid,
    glb_export,
    optimization,
    polycount,
    uv_check
)

classes = (
    ui.Blender2UPreferences,
    ui.OBJECT_PT_Blender2UPanel
)

addons = {
    # analytics,
    auto_scale,
    bake_nodes,
    collection_grid,
    glb_export,
    polycount,
    uv_check,
    # blendercv,
    # mesh_lint,
    # material_library,
    # hh_connect,
    # blenderkit_adapter,
    optimization
}


def register():
    addon_updater_ops.register(bl_info)

    for cls in classes:
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
