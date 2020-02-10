bl_info = {
    "name": "Substance Integration",
    "author": "Real2U",
    "blender": (2, 8, 0),
    "category": "Mesh",
}

import bpy
import os
from .panel import OBJECT_PT_SubstancePanel
from .settings import HHConnectSettings
from .integration import HHPresetsTimerOperator, HHDelMatsOps, HHDelTxtsOps, HHDelAllOps


classes = (
    HHConnectSettings,
    HHPresetsTimerOperator,
    HHDelMatsOps,
    HHDelTxtsOps,
    HHDelAllOps,
    OBJECT_PT_SubstancePanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.hh_settings = bpy.props.PointerProperty(type=HHConnectSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.hh_settings


if __name__ == "__main__":
    register()
