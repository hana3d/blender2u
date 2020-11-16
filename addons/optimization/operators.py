from typing import List

import bpy


def move_objects_to_collections(objects: List[bpy.types.Object], context: bpy.types.Context):
    for obj in objects:
        bpy.ops.object.select_all(action='DESELECT')
        if obj.parent is None:
            original_name = obj.name
            original_coll = obj.users_collection[0]
            context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
            collection = bpy.data.collections.new(original_name)
            context.scene.collection.children.link(collection)
            collection.objects.link(obj)
            bpy.ops.collection.objects_add_active(collection=collection.name)
            bpy.ops.collection.objects_remove(collection=original_coll.name)


def clean_empties():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_by_type(extend=False, type='EMPTY')
    bpy.ops.object.delete()


def join_objects(collections: List[bpy.types.Collection], context: bpy.types.Context):
    for coll in collections:
        if len(coll.objects) == 0:
            bpy.data.collections.remove(coll)
            continue

        bpy.ops.object.select_all(action='DESELECT')
        for obj in coll.objects:
            obj.select_set(True)
            if obj.parent is None:
                context.view_layer.objects.active = obj

        bpy.ops.object.join()

        coll.objects[0].name = coll.name


def mesh_optimization(context: bpy.types.Context):
    if context.mode != 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=True)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.mesh.tris_convert_to_quads()

    bpy.ops.object.editmode_toggle()


def add_modifiers(objects: List[bpy.types.Object], context: bpy.types.Context):
    for obj in objects:
        context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
        obj.modifiers["Decimate"].ratio = 0.1
        obj.modifiers["WeightedNormal"].keep_sharp = True


def resize_image_textures(objects: List[bpy.types.Object]):
    for obj in objects:
        for material_slot in obj.material_slots:
            mat = material_slot.material
            if mat is None:
                continue
            for node in mat.node_tree.nodes:
                if node.type != 'TEX_IMAGE':
                    continue

                if node.image.size[0] > 1024:
                    node.image.scale(1024, 1024)
                    node.image.save()
                    node.image.pack()


class OptimizationOperator(bpy.types.Operator):
    """Automatic Model Optimization"""
    bl_idname = "object.optimization"
    bl_label = "Model Optimization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        move_objects_to_collections(context.scene.objects, context)
        clean_empties()
        join_objects(context.scene.collection.children, context)
        mesh_optimization(context)
        add_modifiers(context.scene.objects, context)
        resize_image_textures(context.scene.objects)

        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except:
            print('Addon analytics not installed')
        return self.execute(context)


classes = (
    OptimizationOperator
)


def register():
    # for cls in classes:
    #     bpy.utils.register_class(cls)
    bpy.utils.register_class(OptimizationOperator)


def unregister():
    # for cls in reversed(classes):
    #     bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(OptimizationOperator)


if __name__ == "__main__":
    register()
