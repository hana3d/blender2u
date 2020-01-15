# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "analytics",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "",
    "warning": "",
    "category": "Mesh"
}

import bpy
from bpy.app.handlers import persistent


class ModalOperator(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):

        return {'FINISHED'}

    def modal(self, context, event):
        if event.type != 'MOUSEMOVE' and event.value != 'RELEASE':
            print(event.type)
            # self.execute(context)

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        # self.execute(context, event)

        return {'RUNNING_MODAL'}


@persistent
def load_handler(dummy):
    bpy.ops.object.modal_operator('INVOKE_DEFAULT')


def register():
    bpy.utils.register_class(ModalOperator)
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.utils.unregister_class(ModalOperator)


if __name__ == "__main__":
    register()
