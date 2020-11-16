bl_info = {
    "name": "nodes-io",
    "author": "R2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Node"
}


import bpy
from .export_nodes import ExportNodes
from .import_nodes import ImportNodes
from .panel import OBJECT_PT_NodesIOPanel


classes = (
    ExportNodes,
    ImportNodes,
    OBJECT_PT_NodesIOPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
