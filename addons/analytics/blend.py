import bpy
import os
import json
import requests
import uuid
from bpy.app.handlers import persistent
from .config import version, api_url, timestamp, user


@persistent
def blend_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.blend_modal('INVOKE_DEFAULT')


class BlendModal(bpy.types.Operator):
    bl_idname = "object.blend_modal"
    bl_label = "Blend Modal Operator"

    def __init__(self):
        print("Start")

        blend_file = bpy.path.basename(bpy.context.blend_data.filepath)
        blender_version = bpy.app.version_string
        event_id = str(uuid.uuid1())

        data = {
            'blend': blend_file,
            'blender_version': blender_version,
            'event_id': event_id,
            'timestamp': timestamp,
            'user': user,
            'version': version,
            'open': 1
        }

        r = requests.post(url=api_url, json=data)
        print(r.status_code)

    def __del__(self):
        print("End")

        blend_file = bpy.path.basename(bpy.context.blend_data.filepath)
        blender_version = bpy.app.version_string
        event_id = str(uuid.uuid1())

        data = {
            'blend': blend_file,
            'blender_version': blender_version,
            'event_id': event_id,
            'timestamp': timestamp,
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
