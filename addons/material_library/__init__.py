bl_info = {
    "name": "Material Library",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Material"
}

import bpy
from .workspace import CreateWorkspace
from . import materials_library_vx
from .panel import MATLIB_PT_MatLibPanel

classes = (
    CreateWorkspace,
    MATLIB_PT_MatLibPanel
)


def register():
    materials_library_vx.register()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    materials_library_vx.unregister()


if __name__ == "__main__":
    register()
