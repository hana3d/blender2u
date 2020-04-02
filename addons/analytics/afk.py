import bpy
import requests
from . import config
from bpy.app.handlers import persistent


@persistent
def afk_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.afk_modal('INVOKE_DEFAULT')


def every_5_minutes():
    if config.is_afk == 1:
        data = config.basic_message()
        data.update({'afk': 1})

        r = requests.post(url=config.api_url, json=data)
        print('AFK')
        print(r.status_code)

    config.is_afk = 1

    return 300


class AfkModal(bpy.types.Operator):
    bl_idname = "analytics.afk_modal"
    bl_label = "Blend Modal Operator"

    def __init__(self):
        bpy.app.timers.register(every_5_minutes, first_interval=300)

    def __del__(self):
        print("Del AFK")

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):
        if config.is_afk == 1:
            print('NOT AFK')
            config.is_afk = 0

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
