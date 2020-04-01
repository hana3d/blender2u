import bpy
import os
from bpy.app.handlers import persistent
from .config import timestamp


@persistent
def event_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.event_modal('INVOKE_DEFAULT')


class EventModal(bpy.types.Operator):
    bl_idname = "analytics.event_modal"
    bl_label = "Event Modal Operator"

    logs_folder = bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' + os.sep \
        + 'blender2u' + os.sep + 'addons' + os.sep + 'analytics' + os.sep + 'logs' + os.sep

    ignored_events = [
        'MOUSEMOVE',
        'TIMER_REPORT'
    ]

    def __init__(self):
        print("Start")
        now = timestamp
        dt_string = now.strftime("%d.%m.%Y")
        self.file = open(self.logs_folder + dt_string + '-' + bpy.path.basename(bpy.context.blend_data.filepath) + '.txt', "a+")

    def __del__(self):
        print("End")
        self.file.close()

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):
        if event.type not in self.ignored_events and event.value != 'RELEASE':
            print(event.type, event.value)
            now = timestamp
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            self.file.write(dt_string + "   " + event.type + "\n")
            # self.execute(context)

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
