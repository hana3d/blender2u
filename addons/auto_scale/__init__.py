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


# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ObjectAutoScale)
    bpy.utils.register_class(ObjectCSVScale)
    bpy.utils.register_class(OBJECT_PT_AutoScalePanel)
    # bpy.types.TOPBAR_MT_edit.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(ObjectAutoScale.bl_idname, 'S', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(ObjectAutoScale)
    bpy.utils.unregister_class(ObjectCSVScale)
    bpy.utils.unregister_class(OBJECT_PT_AutoScalePanel)
    # bpy.types.TOPBAR_MT_edit.remove(menu_func)


if __name__ == "__main__":
    register()
