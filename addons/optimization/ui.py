import bpy


class OBJECT_PT_OptimizationPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Optimization"
    bl_context = "objectmode"
    bl_category = "Real2U"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        global custom_icons

        layout = self.layout

        row = layout.row()
        row.operator('object.optimization', text='Automatic Model Optimization')


classes = (
    OBJECT_PT_OptimizationPanel
)


def register():
    # for cls in classes:
    #     bpy.utils.register_class(cls)
    bpy.utils.register_class(OBJECT_PT_OptimizationPanel)


def unregister():
    # for cls in reversed(classes):
    #     bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(OBJECT_PT_OptimizationPanel)


if __name__ == "__main__":
    register()
