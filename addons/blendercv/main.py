import bpy
from .mesh_contour import MeshContourClass, MeshContourProps
from .canny_edges import CannyEdgesClass, CannyEdgesProps
from .panel import OBJECT_PT_ContourPanel, OBJECT_PT_CannyPanel


classes = (
    MeshContourClass,
    MeshContourProps,
    CannyEdgesClass,
    CannyEdgesProps,
    OBJECT_PT_ContourPanel,
    OBJECT_PT_CannyPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.mesh_contour_props = bpy.props.PointerProperty(type=MeshContourProps)
    bpy.types.Scene.canny_edges_props = bpy.props.PointerProperty(type=CannyEdgesProps)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.mesh_contour_props
    del bpy.types.Scene.canny_edges_props
