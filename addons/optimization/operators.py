import bpy


class OptimizationOperator(bpy.types.Operator):
    """Automatic Model Optimization"""
    bl_idname = "object.optimization"
    bl_label = "Model Optimization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.overlay.show_face_orientation = True

        # TODO move hierarchy
        for obj in context.scene.objects:
            if obj.parent is None:
                collection = bpy.data.collections.new("Collection")
                context.scene.collection.children.link(collection)
                collection.objects.link(obj)

        # TODO clean empties

        for coll in context.scene.collection.children:
            if len(coll.children) == 0:
                bpy.data.collections.remove(coll)
                continue

            bpy.ops.object.select_all(action='DESELECT')
            for obj in coll.objects:
                obj.select_set(True)
                if obj.parent is None:
                    context.view_layer.objects.active = obj

            bpy.ops.object.join()

        bpy.ops.object.select_all(action='SELECT')

        if context.mode != 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=True)
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        bpy.ops.mesh.tris_convert_to_quads()

        for obj in context.scene.objects:
            context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
            obj.modifiers["Decimate"].ratio = 0.1
            obj.modifiers["WeightedNormal"].keep_sharp = True

        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except:
            print('Addon analytics not installed')
        return {'RUNNING_MODAL'}


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
