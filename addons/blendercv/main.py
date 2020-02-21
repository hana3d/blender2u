import bpy
from .mesh_contour import MeshContourClass
from .canny_edges import CannyEdgesClass
from .panel import OBJECT_PT_ContourPanel, OBJECT_PT_CannyPanel


classes = (
    MeshContourClass,
    CannyEdgesClass,
    OBJECT_PT_ContourPanel,
    OBJECT_PT_CannyPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
