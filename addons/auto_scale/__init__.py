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
    "name": "auto-scale",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "version": (1, 2, 0),
    "location": "",
    "warning": "",
    "category": "Object"
}

import bpy
from .user import ObjectAutoScale
from .csv import ObjectCSVScale
from .panel import OBJECT_PT_AutoScalePanel


def menu_func(self, context):
    self.layout.operator(ObjectAutoScale.bl_idname)
    self.layout.operator(ObjectCSVScale.bl_idname)


def register():
    bpy.utils.register_class(ObjectAutoScale)
    bpy.utils.register_class(ObjectCSVScale)
    bpy.utils.register_class(OBJECT_PT_AutoScalePanel)
    # bpy.types.TOPBAR_MT_edit.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ObjectAutoScale)
    bpy.utils.unregister_class(ObjectCSVScale)
    bpy.utils.unregister_class(OBJECT_PT_AutoScalePanel)
    # bpy.types.TOPBAR_MT_edit.remove(menu_func)


if __name__ == "__main__":
    register()
