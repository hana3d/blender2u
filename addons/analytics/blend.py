import bpy
import os
import json
import requests
from bpy.app.handlers import persistent
from .config import version, api_url, user, get_blend_file, get_blender_version, get_timestamp, get_uuid


@persistent
def blend_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.blend_modal('INVOKE_DEFAULT')


class BlendModal(bpy.types.Operator):
    bl_idname = "object.blend_modal"
    bl_label = "Blend Modal Operator"

    def __init__(self):
        print("Start")

        self.session_id = get_uuid()

        data = {
            'blend': get_blend_file(),
            'blender_version': get_blender_version(),
            'event_id': get_uuid(),
            'session_id': self.session_id,
            'timestamp': get_timestamp(),
            'user': user,
            'version': version,
            'open': 1
        }

        r = requests.post(url=api_url, json=data)
        print(r.status_code)

        bpy.app.timers.register(self.every_10_minutes, first_interval=600)

    def __del__(self):
        print("End")

        data = {
            'blend': get_blend_file(),
            'blender_version': get_blender_version(),
            'event_id': get_uuid(),
            'session_id': self.session_id,
            'timestamp': get_timestamp(),
            'user': user,
            'version': version,
            'close': 1
        }

        r = requests.post(url=api_url, json=data)
        print(r.status_code)

        bpy.app.timers.unregister(self.every_10_minutes)

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def every_10_minutes(self):
        data = {
            'blend': get_blend_file(),
            'blender_version': get_blender_version(),
            'event_id': get_uuid(),
            'session_id': self.session_id,
            'timestamp': get_timestamp(),
            'user': user,
            'version': version,
            'ping': 1
        }

        r = requests.post(url=api_url, json=data)
        print('Ping')
        print(r.status_code)

        return 600
