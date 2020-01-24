import bpy
import os
import json
import requests
from bpy.app.handlers import persistent
from .config import version, api_url, user, session_id, get_blend_file, get_blender_version, get_collections, get_objects, get_timestamp, get_uuid


@persistent
def blend_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.blend_modal('INVOKE_DEFAULT')


def every_10_minutes():
    data = {
        'blend': get_blend_file(),
        'blender_version': get_blender_version(),
        'collections_count': get_collections(),
        'event_id': get_uuid(),
        'objects_count': get_objects(),
        'session_id': session_id,
        'timestamp': get_timestamp(),
        'user': user,
        'version': version,
        'ping': 1
    }

    r = requests.post(url=api_url, json=data)
    print('Ping')
    print(r.status_code)

    return 600


class BlendModal(bpy.types.Operator):
    bl_idname = "object.blend_modal"
    bl_label = "Blend Modal Operator"

    def __init__(self):
        print("Start")

        self.session_id = get_uuid()

        data = {
            'blend': get_blend_file(),
            'blender_version': get_blender_version(),
            'collections_count': get_collections(),
            'event_id': get_uuid(),
            'objects_count': get_objects(),
            'session_id': session_id,
            'timestamp': get_timestamp(),
            'user': user,
            'version': version,
            'open': 1
        }

        r = requests.post(url=api_url, json=data)
        print(r.status_code)

        bpy.app.timers.register(every_10_minutes, first_interval=600)

    def __del__(self):
        print("End")

        bpy.app.timers.unregister(every_10_minutes)

        data = {
            'blend': get_blend_file(),
            'blender_version': get_blender_version(),
            'collections_count': get_collections(),
            'event_id': get_uuid(),
            'objects_count': get_objects(),
            'session_id': session_id,
            'timestamp': get_timestamp(),
            'user': user,
            'version': version,
            'close': 1
        }

        r = requests.post(url=api_url, json=data)
        print(r.status_code)

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
