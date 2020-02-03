bl_info = {
    "name": "Computer-Vision",
    "author": "Real2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "category": "System"
}


import os
import sys
import bpy
from . import environment
from .opencv import OpencvClass
# from .libs.replication.replication.constants import RP_COMMON


# TODO: remove dependency as soon as replication will be installed as a module
DEPENDENCIES = {
    ("opencv", "opencv-python")
}

# TODO: refactor config
# UTILITY FUNCTIONS
classes = (
)

# libs = os.path.dirname(os.path.abspath(__file__)) + "\\libs\\replication"


def register():
    # if libs not in sys.path:
    #     sys.path.append(libs)

    environment.setup(DEPENDENCIES, bpy.app.binary_path_python)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
