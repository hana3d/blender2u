import operator
import bpy
from mathutils import Color


class ColorObjects(bpy.types.Operator):
    """Color Objects"""
    bl_idname = "object.color_objects"
    bl_label = "Color Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        coll = bpy.context.view_layer.active_layer_collection.collection

        total_polygons = 0
        results = {}
        for obj in coll.objects:
            if hasattr(obj.data, 'polygons') and obj.hide_get() is False:
                if 'Decimate' in obj.modifiers:
                    results[obj.name] = obj.modifiers["Decimate"].face_count
                    total_polygons += obj.modifiers["Decimate"].face_count
                else:
                    results[obj.name] = len(obj.data.polygons)
                    total_polygons += len(obj.data.polygons)

        sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

        top_result = sorted_results[0][1]
        last_result = sorted_results[-1][1]

        if top_result == last_result:
            print('All objects have the same number of polygons')
            return {'FINISHED'}

        for result in sorted_results:
            obj = bpy.context.scene.objects[result[0]]

            if obj.active_material is None:
                obj.original_material.add().add(None)
            elif "PKHG" not in obj.active_material.name:
                obj.original_material.clear()
                for material_slots in obj.material_slots:
                    obj.original_material.add().add(material_slots.material)
                obj.data.materials.clear()
            else:
                active_material = obj.active_material
                obj.data.materials.clear()
                bpy.data.materials.remove(active_material)

            c = Color()
            c.hsv = (0.0, (result[1] - last_result) / (top_result - last_result), 1.0)

            mat = bpy.data.materials.new("PKHG")
            mat.diffuse_color = (c.r, c.g, c.b, 1.0)
            obj.active_material = mat

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[sorted_results[0][0]].select_set(True)
        bpy.ops.view3d.view_selected()

        return {'FINISHED'}


class OriginalColor(bpy.types.Operator):
    """Original Color"""
    bl_idname = "object.original_color"
    bl_label = "Original Color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        coll = bpy.context.view_layer.active_layer_collection.collection

        for obj in coll.objects:
            if hasattr(obj.data, 'polygons') and len(obj.original_material) > 0:
                if obj.original_material[0].material != obj.active_material:
                    active_material = obj.active_material
                    obj.data.materials.clear()
                    bpy.data.materials.remove(active_material)
                    for material_slots in obj.original_material:
                        obj.data.materials.append(material_slots.material)

        return {'FINISHED'}
