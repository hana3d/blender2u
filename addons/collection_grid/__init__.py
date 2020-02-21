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
import bpy
from mathutils import Vector
from .panel import OBJECT_PT_CollectionGridPanel


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

        context.view_layer.active_layer_collection = context.scene.view_layers[0].layer_collection

        rows = scene.collection_grid_props.rows
        distance = scene.collection_grid_props.distance
        switch = scene.collection_grid_props.switch

        try:
            bpy.ops.object.select_all(action='SELECT')
            print('select')
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            print('clear parent')
            bpy.ops.object.select_by_type(extend=False, type='EMPTY')
            print('select empty')
            bpy.ops.object.delete(use_global=True, confirm=False)
        except:
            print('No empties')

        row_position = 0
        collumn_position = 0

        if switch is True:
            objects = bpy.context.scene.objects
            collumns = math.ceil(len(objects) / rows)

            bpy.ops.object.select_all(action='DESELECT')
            for obj in objects:
                if (obj.visible_get()):
                    obj.select_set(True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=False)

                    min_x = 999999
                    min_y = 999999
                    min_z = 999999
                    max_x = -999999
                    max_y = -999999
                    max_z = -999999

                    for vertex in [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]:
                        min_x = (min_x, vertex[0])[vertex[0] < min_x]
                        min_y = (min_y, vertex[1])[vertex[1] < min_y]
                        min_z = (min_z, vertex[2])[vertex[2] < min_z]
                        max_x = (max_x, vertex[0])[vertex[0] > max_x]
                        max_y = (max_y, vertex[1])[vertex[1] > max_y]
                        max_z = (max_z, vertex[2])[vertex[2] > max_z]

                    bpy.ops.object.select_all(action='DESELECT')

                    center_x = min_x + (max_x - min_x) / 2
                    center_y = min_y + (max_y - min_y) / 2
                    bpy.ops.object.add(type='EMPTY', location=(center_x, center_y, min_z))
                    empty = bpy.context.selected_objects[0]
                    bpy.context.view_layer.objects.active = empty

                    obj.select_set(True)
                    bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
                    bpy.ops.object.select_all(action='DESELECT')
                    empty.select_set(True)

                    empty.location.x = - ((collumns - 1) / 2) * distance + collumn_position * distance
                    empty.location.y = - (- ((rows - 1) / 2) * distance + row_position * distance)
                    empty.location.z = 0
                    if collumn_position != (collumns - 1):
                        collumn_position = collumn_position + 1
                    else:
                        row_position = row_position + 1
                        collumn_position = 0

                    bpy.ops.object.select_all(action='DESELECT')

        else:
            collections = bpy.data.collections
            collumns = math.ceil(len(collections) / rows)

            bpy.ops.object.select_all(action='DESELECT')
            for coll in collections:
                print(coll.name)

                min_x = 999999
                min_y = 999999
                min_z = 999999
                max_x = -999999
                max_y = -999999
                max_z = -999999

                valid_object = False

                for obj in coll.objects:
                    if (obj.visible_get()):
                        valid_object = True
                        obj.select_set(True)
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=False)

                        for vertex in [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]:
                            min_x = (min_x, vertex[0])[vertex[0] < min_x]
                            min_y = (min_y, vertex[1])[vertex[1] < min_y]
                            min_z = (min_z, vertex[2])[vertex[2] < min_z]
                            max_x = (max_x, vertex[0])[vertex[0] > max_x]
                            max_y = (max_y, vertex[1])[vertex[1] > max_y]
                            max_z = (max_z, vertex[2])[vertex[2] > max_z]

                        bpy.ops.object.select_all(action='DESELECT')

                if not valid_object:
                    continue

                center_x = min_x + (max_x - min_x) / 2
                center_y = min_y + (max_y - min_y) / 2
                bpy.ops.object.add(type='EMPTY', location=(center_x, center_y, min_z))
                empty = bpy.context.selected_objects[0]
                coll.objects.link(empty)
                bpy.context.view_layer.active_layer_collection.collection.objects.unlink(empty)

                bpy.context.view_layer.objects.active = empty

                bpy.ops.object.select_all(action='DESELECT')
                for obj in coll.objects:
                    if obj != empty:
                        if (obj.visible_get()):
                            obj.select_set(True)

                bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
                bpy.ops.object.select_all(action='DESELECT')
                empty.select_set(True)

                empty.location.x = - ((collumns - 1) / 2) * distance + collumn_position * distance
                empty.location.y = - (- ((rows - 1) / 2) * distance + row_position * distance)
                empty.location.z = 0
                if collumn_position != (collumns - 1):
                    collumn_position = collumn_position + 1
                else:
                    row_position = row_position + 1
                    collumn_position = 0

                bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.select_all(action='SELECT')
        print('select')
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        print('clear parent')
        bpy.ops.object.select_by_type(extend=False, type='EMPTY')
        print('select empty')
        bpy.ops.object.delete(use_global=True, confirm=False)
        print('delete')
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
