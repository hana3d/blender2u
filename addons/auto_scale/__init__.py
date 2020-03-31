bl_info = {
    "name": "auto-scale",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Object"
}

import bpy
from .user import ObjectAutoScale, AutoScaleProps
from .csv import ObjectCSVScale
from .panel import OBJECT_PT_AutoScalePanel


def register():
    bpy.utils.register_class(AutoScaleProps)
    bpy.utils.register_class(ObjectAutoScale)
    bpy.utils.register_class(ObjectCSVScale)
    bpy.utils.register_class(OBJECT_PT_AutoScalePanel)

    bpy.types.Scene.auto_scale_props = bpy.props.PointerProperty(type=AutoScaleProps)


def unregister():
    del bpy.types.Scene.auto_scale_props

    bpy.utils.unregister_class(OBJECT_PT_AutoScalePanel)
    bpy.utils.unregister_class(ObjectCSVScale)
    bpy.utils.unregister_class(ObjectAutoScale)
    bpy.utils.unregister_class(AutoScaleProps)


if __name__ == "__main__":
    register()
