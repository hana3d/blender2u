import bpy
import requests
from bpy.app.handlers import persistent
from .config import api_url, basic_message


@persistent
def blend_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.blend_modal('INVOKE_DEFAULT')


@persistent
def save_handler(dummy):
    data = basic_message()
    data.update({'save': 1})

    r = requests.post(url=api_url, json=data)
    print('Save')
    print(r.status_code)


def every_10_minutes():
    data = basic_message()
    data.update({'ping': 1})

    r = requests.post(url=api_url, json=data)
    print('Ping')
    print(r.status_code)

    return 600


class BlendModal(bpy.types.Operator):
    bl_idname = "analytics.blend_modal"
    bl_label = "Blend Modal Operator"

    def __init__(self):
        print("Start")

        data = basic_message()
        data.update({'open': 1})

        r = requests.post(url=api_url, json=data)
        print(r.status_code)

        bpy.app.timers.register(every_10_minutes, first_interval=600)

    def __del__(self):
        print("End")

        data = basic_message()
        data.update({'close': 1})

        r = requests.post(url=api_url, json=data)
        print(r.status_code)

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
