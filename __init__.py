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
    "name": "Blender2U",
    "author": "Real2U",
    "description": "Tools developed by Real2U",
    "blender": (2, 80, 0),
    "version": (0, 1, 1),
    "location": "",
    "warning": "",
    "wiki_url": "https://gitlab.com/real2u/blender2u",
    "category": "System"
}

import math
import bpy
from . import addon_updater_ops
from .addons import glb_usdz_export
from .addons import glb_export
from .preferences import Blender2UPreferences
# from .glb_usdz_export import GLBUSDZExport
from .panel import OBJECT_PT_Blender2UPanel


classes = (
    Blender2UPreferences,
    # glb_usdz_export.GLBUSDZExport,
    OBJECT_PT_Blender2UPanel
)

addons = {
    glb_usdz_export,
    glb_export
}


def register():
    addon_updater_ops.register(bl_info)

    for addon in addons:
        addon.register()

    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)


def unregister():
    addon_updater_ops.unregister()

    for addon in addons:
        addon.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
