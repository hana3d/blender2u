bl_info = {
    "name": "material_library",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Material"
}

# from .workspace import OBJECT_PT_Mat_Lib_Workspace
from . import materials_library_vx
import bpy

classes = (
    # OBJECT_PT_Mat_Lib_Workspace
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
