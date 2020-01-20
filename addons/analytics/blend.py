import bpy
import os
import datetime
import json
import requests
import getpass


def blend_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) == '':
        bpy.ops.object.modal_operator('INVOKE_DEFAULT')


class EventModal(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    URL = "https://api.real2u.com.br/blender"

    user = getpass.getuser()

    logs_folder = bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' + os.sep \
        + 'analytics' + os.sep + 'logs' + os.sep
    # + os.sep + 'blender2u' + os.sep + 'addons' + os.sep

    def __init__(self):
        print("Start")
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        data = {
            'blend': bpy.path.basename(bpy.context.blend_data.filepath),
            'operation': 'open',
            'date': date,
            'eventId': uuid,
            'time': time,
            'user': self.user
        }

        r = requests.post(url=self.URL, json=data)
        print(r.status_code)

    def __del__(self):
        print("End")
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        data = {
            'blend': bpy.path.basename(bpy.context.blend_data.filepath),
            'operation': 'close',
            'time': dt_string,
            'user': self.user
        }

        r = requests.post(url=self.URL, json=data)
        print(r.status_code)

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
