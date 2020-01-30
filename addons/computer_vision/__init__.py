bl_info = {
    "name": "Computer-Vision",
    "author": "Real2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "Unstable addon, use it at your own risks",
    "category": "System"
}


import os
import sys

import bpy
from bpy.app.handlers import persistent

from . import environment, utils, presence, operators, ui
from .libs.replication.replication.constants import RP_COMMON


# TODO: remove dependency as soon as replication will be installed as a module
DEPENDENCIES = {
    ("opencv", "opencv-python")
}


# TODO: refactor config
# UTILITY FUNCTIONS
classes = (

)

libs = os.path.dirname(os.path.abspath(__file__)) + "\\libs\\replication"


@persistent
def load_handler(dummy):
    import bpy
    bpy.context.window_manager.session.load()


def register():
    if libs not in sys.path:
        sys.path.append(libs)

    environment.setup(DEPENDENCIES, bpy.app.binary_path_python)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.context.window_manager.session.load()

    presence.register()
    operators.register()
    ui.register()
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    presence.unregister()
    ui.unregister()
    operators.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
