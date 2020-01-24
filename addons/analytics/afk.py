import bpy
import os
import json
import requests
import config
from bpy.app.handlers import persistent


@persistent
def afk_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.afk_modal('INVOKE_DEFAULT')


def every_5_minutes():
    if config.is_afk == 1:
        data = config.basic_message
        data.update({'afk': 1})
    else:
        config.is_afk = 1

    return 300


class AfkModal(bpy.types.Operator):
    bl_idname = "object.blend_modal"
    bl_label = "Blend Modal Operator"

    def __init__(self):
        bpy.app.timers.register(every_5_minutes, first_interval=300)

    def __del__(self):
        bpy.app.timers.unregister(every_5_minutes)

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):
        config.is_afk = 0

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
