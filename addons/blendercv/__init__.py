bl_info = {
    "name": "BlenderCV",
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
from .mesh_contour import MeshContourClass, MeshContourProps
from .canny_edges import CannyEdgesClass, CannyEdgesProps
from .panel import OBJECT_PT_ContourPanel, OBJECT_PT_CannyPanel
# from .libs.replication.replication.constants import RP_COMMON


# TODO: remove dependency as soon as replication will be installed as a module
DEPENDENCIES = {
    ("opencv", "opencv-python")
}

# TODO: refactor config
# UTILITY FUNCTIONS
classes = (
    MeshContourClass,
    MeshContourProps,
    CannyEdgesClass,
    CannyEdgesProps,
    OBJECT_PT_ContourPanel,
    OBJECT_PT_CannyPanel
)

# libs = os.path.dirname(os.path.abspath(__file__)) + "\\libs\\replication"


def register():
    # if libs not in sys.path:
    #     sys.path.append(libs)

    environment.setup(DEPENDENCIES, bpy.app.binary_path_python)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.mesh_contour_props = bpy.props.PointerProperty(type=MeshContourProps)
    bpy.types.Scene.canny_edges_props = bpy.props.PointerProperty(type=CannyEdgesProps)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.mesh_contour_props
    del bpy.types.Scene.canny_edges_props
