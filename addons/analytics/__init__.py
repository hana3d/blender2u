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


class LogCommands(bpy.types.Operator):
    """Log Commands"""
    bl_idname = "object.log_commands"
    bl_label = "Log Commands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(LogCommands.bl_idname)


def register():
    bpy.utils.register_class(LogCommands)
    # bpy.types.TOPBAR_MT_edit.append(menu_func)


def unregister():
    # bpy.types.TOPBAR_MT_edit.remove(menu_func)
    bpy.utils.unregister_class(LogCommands)


if __name__ == "__main__":
    register()
