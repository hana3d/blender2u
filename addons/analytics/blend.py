import bpy
import os
import datetime
import json
import requests
import getpass
import config


def blend_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) == '':
        bpy.ops.object.modal_operator('INVOKE_DEFAULT')


class EventModal(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def __init__(self):
        print("Start")

        data = {
            'blend': config.blend_file,
            'event_id': config.event_id,
            'timestamp': config.timestamp,
            'user': config.user,
            'version': config.version,
            'open': 1
        }

        r = requests.post(url=config.api_url, json=data)
        print(r.status_code)

    def __del__(self):
        print("End")

        data = {
            'blend': config.blend_file,
            'event_id': config.event_id,
            'timestamp': config.timestamp,
            'user': config.user,
            'version': config.version,
            'close': 1
        }

        r = requests.post(url=config.api_url, json=data)
        print(r.status_code)

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
