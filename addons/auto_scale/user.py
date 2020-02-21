import bpy
from mathutils import Vector


class AutoScaleProps(bpy.types.PropertyGroup):
    height: bpy.props.FloatProperty(
        name="Height",
        description="Height of the object",
        default=1.0
    )

    length: bpy.props.FloatProperty(
        name="Length",
        description="Length of the object",
        default=1.0
    )

    switch: bpy.props.BoolProperty(
        name="Use length",
        description="Use length value instead of height",
        default=False
    )


class ObjectAutoScale(bpy.types.Operator):
    """Object Auto Scale"""
    bl_idname = "object.auto_scale"
    bl_label = "Automatic Scale"
    bl_options = {'REGISTER', 'UNDO'}

    height: bpy.props.FloatProperty(name="Height:", default=0.0)
    length: bpy.props.FloatProperty(name="Length:", default=0.0)
    switch: bpy.props.BoolProperty(name="Use length", description="", default=False)

    def execute(self, context):
        scene = context.scene

        final_z = scene.auto_scale_props.height
        final_x = scene.auto_scale_props.length

        min_x = 999999
        min_y = 999999
        min_z = 999999
        max_x = -999999
        max_y = -999999
        max_z = -999999

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)
        for obj in bpy.context.selected_objects:
            if obj.visible_get() and obj.type != 'EMPTY':

                for vertex in [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]:
                    min_x = (min_x, vertex[0])[vertex[0] < min_x]
                    min_y = (min_y, vertex[1])[vertex[1] < min_y]
                    min_z = (min_z, vertex[2])[vertex[2] < min_z]
                    max_x = (max_x, vertex[0])[vertex[0] > max_x]
                    max_y = (max_y, vertex[1])[vertex[1] > max_y]
                    max_z = (max_z, vertex[2])[vertex[2] > max_z]

        if scene.auto_scale_props.switch is False:
            size_z = max_z - min_z
            scale = final_z / size_z
        else:
            size_x = max_x - min_x
            size_y = max_y - min_y
            scale = (final_x / size_x) if (size_x > size_y) else (final_x / size_y)

        bpy.ops.transform.resize(value=(scale, scale, scale))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)
        return {'FINISHED'}
