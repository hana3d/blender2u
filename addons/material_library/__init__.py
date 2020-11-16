bl_info = {
    "name": "Material Library",
    "author": "R2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Material"
}

import bpy
from .scene import CreateScene
from . import materials_library_vx
from .api import S3Download, S3Upload
from .panel import MATLIB_PT_MatLibPanel, MATLIB_PT_PreviewPanel, UpdatePreview

classes = (
    CreateScene,
    S3Download,
    S3Upload,
    MATLIB_PT_MatLibPanel,
    MATLIB_PT_PreviewPanel,
    UpdatePreview
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
