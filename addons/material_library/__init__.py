bl_info = {
    "name": "material_library",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "System"
}

import bpy
from .workspace import OBJECT_PT_Mat_Lib_Workspace


classes = (
    OBJECT_PT_Mat_Lib_Workspace
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
