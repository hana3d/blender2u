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
# from .workspace import OBJECT_PT_Mat_Lib_Workspace
from . import materials_library_vx
from .panel import MATLIB_PT_MatLibPanel

classes = (
    # OBJECT_PT_Mat_Lib_Workspace
    # OBJECT_PT_MatLibPanel
)


def register():
    materials_library_vx.register()
    # for cls in classes:
    #     bpy.utils.register_class(cls)
    bpy.utils.register_class(MATLIB_PT_MatLibPanel)


def unregister():
    # for cls in reversed(classes):
    #     bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(MATLIB_PT_MatLibPanel)
    materials_library_vx.unregister()


if __name__ == "__main__":
    register()
