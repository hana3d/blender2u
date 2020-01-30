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

from . import environment, utils, presence
from .libs.replication.replication.constants import RP_COMMON


# TODO: remove dependency as soon as replication will be installed as a module
DEPENDENCIES = {
    ("opencv", "opencv-python")
}


# TODO: refactor config
# UTILITY FUNCTIONS
class ReplicatedDatablock(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    type_name: bpy.props.StringProperty()
    bl_name: bpy.props.StringProperty()
    bl_delay_refresh: bpy.props.FloatProperty()
    bl_delay_apply: bpy.props.FloatProperty()
    use_as_filter: bpy.props.BoolProperty(default=True)
    auto_push: bpy.props.BoolProperty(default=True)
    icon: bpy.props.StringProperty()


classes = (
    ReplicatedDatablock
)

libs = os.path.dirname(os.path.abspath(__file__)) + "\\libs\\replication"


@persistent
def load_handler(dummy):
    import bpy
    bpy.context.window_manager.session.load()


def register():
    if libs not in sys.path:
        sys.path.append(libs)

    environment.setup(DEPENDENCIES,bpy.app.binary_path_python)

    from . import presence
    from . import operators
    from . import ui

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.session = bpy.props.PointerProperty(
        type=SessionProps)
    bpy.types.ID.uuid = bpy.props.StringProperty(default="")

    bpy.context.window_manager.session.load()

    presence.register()
    operators.register()
    ui.register()
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    from . import presence
    from . import operators
    from . import ui

    presence.unregister()
    ui.unregister()
    operators.unregister()

    del bpy.types.WindowManager.session

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
