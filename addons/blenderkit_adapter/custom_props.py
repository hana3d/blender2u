import bpy


class BlenderkitCustomProps(bpy.types.PropertyGroup):
    key: bpy.props.StringProperty(
        name="Key",
        description="Name of new property",
        default='client'
    )

    value: bpy.props.StringProperty(
        name="Value",
        description="Value of new property",
        default='Real2U'
    )


class ModelCreateCustomProps(bpy.types.Operator):
    """Model Create Custom Props"""
    bl_idname = "blenderkit.model_custom_props"
    bl_label = "Model Custom Props"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        obj = context.active_object

        key = scene.blenderkit_custom_props.key
        value = scene.blenderkit_custom_props.value

        obj.blenderkit.custom_props[key] = value
        return {'FINISHED'}


class MaterialCreateCustomProps(bpy.types.Operator):
    """Material Create Custom Props"""
    bl_idname = "blenderkit.material_custom_props"
    bl_label = "Material Custom Props"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        mat = context.active_object.active_material

        key = scene.blenderkit_custom_props.key
        value = scene.blenderkit_custom_props.value

        mat.blenderkit.custom_props[key] = value
        return {'FINISHED'}


class CustomPropsPropertyGroup(bpy.types.PropertyGroup):
    props_number: bpy.props.IntProperty()


def register():
    bpy.utils.register_class(BlenderkitCustomProps)
    bpy.utils.register_class(ModelCreateCustomProps)
    bpy.utils.register_class(MaterialCreateCustomProps)
    bpy.utils.register_class(CustomPropsPropertyGroup)

    bpy.types.Scene.blenderkit_custom_props = bpy.props.PointerProperty(type=BlenderkitCustomProps)


def unregister():
    del bpy.types.Scene.blenderkit_custom_props

    bpy.utils.unregister_class(BlenderkitCustomProps)
    bpy.utils.unregister_class(ModelCreateCustomProps)
    bpy.utils.unregister_class(MaterialCreateCustomProps)
    bpy.utils.unregister_class(CustomPropsPropertyGroup)
