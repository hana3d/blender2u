bl_info = {
    "name": "import-materials",
    "author": "Real2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Material"
}


import bpy
from .single_material import SingleMaterial
from .multiple_materials import MultipleMaterials
from .panel import OBJECT_PT_ImportMaterialPanel


classes = (
    SingleMaterial,
    MultipleMaterials,
    OBJECT_PT_ImportMaterialPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
