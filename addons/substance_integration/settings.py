import bpy


class HHConnectSettings(bpy.types.PropertyGroup):

    active: bpy.props.BoolProperty(
        name="Listen connections",
        description="Enable/Disable Hedgehog Connect service",
        default=False
    )

    time: bpy.props.FloatProperty(
        name="Interval",
        description="Set the listening time interval (seconds) for the Hedgehog Connect service",
        default=0.1
    )
