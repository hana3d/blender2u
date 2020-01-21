import bpy
import os
import json
import requests
from bpy.app.handlers import persistent
from .config import version, api_url, event_id, timestamp, user


@persistent
def report_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) != '':
        bpy.ops.object.report_modal('INVOKE_DEFAULT')


class ReportModal(bpy.types.Operator):
    bl_idname = "object.report_modal"
    bl_label = "Report Modal Operator"

    logs_folder = bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' + os.sep \
        + 'blender2u' + os.sep + 'addons' + os.sep + 'analytics' + os.sep + 'logs' + os.sep

    def __init__(self):
        print("Start")
        now = timestamp
        dt_string = now.strftime("%d.%m.%Y")
        self.file = open(self.logs_folder + dt_string + '-' + bpy.path.basename(bpy.context.blend_data.filepath) + '.txt', "a+")

    def __del__(self):
        print("End")
        self.file.close()

    def execute(self, context):
        # save the current area
        area = bpy.context.area.type

        # set the context
        bpy.context.area.type = 'INFO'

        bpy.ops.info.select_all(action='SELECT')
        bpy.ops.info.report_copy()
        bpy.ops.info.report_delete()

        # leave the context where it was
        bpy.context.area.type = area

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
