import bpy
import os
import datetime
import json


def blend_handler(dummy):
    if bpy.path.basename(bpy.context.blend_data.filepath) == '':
        bpy.ops.object.modal_operator('INVOKE_DEFAULT')


class EventModal(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    logs_folder = bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' + os.sep \
        + 'analytics' + os.sep + 'logs' + os.sep
    # + os.sep + 'blender2u' + os.sep + 'addons' + os.sep

    def __init__(self):
        print("Start")
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        data = {}
        data = []
        data.append({
            'blend': bpy.path.basename(bpy.context.blend_data.filepath),
            'operation': 'open',
            'time': dt_string
        })

        # self.file = open(self.logs_folder + bpy.path.basename(bpy.context.blend_data.filepath) + '.txt', "a+")
        # self.file.write("OPEN" + "   " + bpy.path.basename(bpy.context.blend_data.filepath) + "   " + dt_string + "\n")
        # self.file.close()

    def __del__(self):
        print("End")
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        data = {}
        data = []
        data.append({
            'blend': bpy.path.basename(bpy.context.blend_data.filepath),
            'operation': 'close',
            'time': dt_string
        })

        # self.file = open(self.logs_folder + bpy.path.basename(bpy.context.blend_data.filepath) + '.txt', "a+")
        # self.file.write("CLOSE" + "   " + bpy.path.basename(bpy.context.blend_data.filepath) + "   " + dt_string + "\n")
        # self.file.close()

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
