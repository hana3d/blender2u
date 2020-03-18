bl_info = {
    "name": "collection-grid",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Object"
}

import math
from typing import Tuple, Union

import bpy
from mathutils import Vector

from .panel import OBJECT_PT_CollectionGridPanel


def is_valid_object(obj):
    return obj.visible_get() and obj.type not in ('EMPTY', 'CAMERA')


def get_loc_dim(element: Union[bpy.types.Collection, bpy.types.Object]) -> Tuple[Vector, Vector]:
    """Return pair of vectors with element's median location and dimensions in world coordinates

    Returns:
        Tuple[Vector, Vector] -- First vector contains location, second vector contains dimensions
    """
    if isinstance(element, bpy.types.Object):
        vertices = [element.matrix_world @ Vector(corner) for corner in element.bound_box]
    elif isinstance(element, bpy.types.Collection):
        vertices = []
        for obj in element.objects:
            if not is_valid_object(obj):
                continue
            for corner in obj.bound_box:
                vertices.append(obj.matrix_world @ Vector(corner))

    else:
        raise TypeError('Element must be a blender Collection or Object')
    min_x = min(vertex.x for vertex in vertices)
    min_y = min(vertex.y for vertex in vertices)
    min_z = min(vertex.z for vertex in vertices)
    max_x = max(vertex.x for vertex in vertices)
    max_y = max(vertex.y for vertex in vertices)
    max_z = max(vertex.z for vertex in vertices)

    location = Vector([(max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2])
    dimensions = Vector([max_x - min_x, max_y - min_y, max_z - min_z])

    return location, dimensions


def get_translation_vector(
        element: Union[bpy.types.Collection, bpy.types.Object],
        distance: float,
        columns: int,
        rows: int,
        column_position: int,
        row_position: int) -> Vector:
    location, dimensions = get_loc_dim(element)

    new_location = Vector([
        distance * ((1 - columns) / 2 + column_position),
        distance * ((rows - 1) / 2 - row_position),
        dimensions.z / 2
    ])
    return new_location - location


def next_column_row(columns, column_position, row_position) -> Tuple[int, int]:
    if column_position != (columns - 1):
        column_position += 1
    else:
        row_position += 1
        column_position = 0
    return column_position, row_position


def cleanup_scene(scene):
    for obj in scene.objects:
        if obj.type == 'EMPTY':
            obj.hide_set(True)


class CollectionGridProps(bpy.types.PropertyGroup):
    rows: bpy.props.IntProperty(
        name="Rows",
        description="Number of rows",
        default=3
    )

    distance: bpy.props.FloatProperty(
        name="Distance",
        description="Distance between objects",
        default=1.0
    )

    switch: bpy.props.BoolProperty(
        name="Objects Grid",
        description="Order objects instead of collections",
        default=False
    )


class CollectionGrid(bpy.types.Operator):
    """Collection Grid"""
    bl_idname = "object.collection_grid"
    bl_label = "Collection Grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        context.view_layer.active_layer_collection = scene.view_layers[0].layer_collection

        rows = scene.collection_grid_props.rows
        distance = scene.collection_grid_props.distance
        flag_object_grid = scene.collection_grid_props.switch

        cleanup_scene(scene)

        row_position = 0
        column_position = 0

        if flag_object_grid:
            columns = math.ceil(len(scene.objects) / rows)
            for obj in scene.objects:
                translation = get_translation_vector(
                    obj, distance, columns, rows, column_position, row_position)
                obj.location += translation

                column_position, row_position = next_column_row(columns, column_position, row_position)
        else:
            columns = math.ceil(len(scene.collection.children) / rows)
            for coll in scene.collection.children:
                valid_collection = any(is_valid_object(obj) for obj in coll.objects)
                if not valid_collection:
                    continue

                translation = get_translation_vector(
                    coll, distance, columns, rows, column_position, row_position)

                for obj in coll.objects:
                    if obj.parent is None:
                        obj.location += translation

                column_position, row_position = next_column_row(columns, column_position, row_position)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(CollectionGridProps)
    bpy.utils.register_class(CollectionGrid)
    bpy.utils.register_class(OBJECT_PT_CollectionGridPanel)

    bpy.types.Scene.collection_grid_props = bpy.props.PointerProperty(type=CollectionGridProps)


def unregister():
    del bpy.types.Scene.collection_grid_props

    bpy.utils.unregister_class(OBJECT_PT_CollectionGridPanel)
    bpy.utils.unregister_class(CollectionGrid)
    bpy.utils.unregister_class(CollectionGridProps)


if __name__ == "__main__":
    register()
