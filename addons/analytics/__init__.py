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
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "category": "System"
}

import bpy
from .blend import blend_handler, save_handler, BlendModal
from .afk import afk_handler, AfkModal
from .addons import AddonsAnalytics
# from .events import event_handler, EventModal
# from .reports import report_handler, ReportModal

classes = (
    AddonsAnalytics,
    BlendModal,
    # ReportModal,
    # EventModal,
    AfkModal
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.handlers.load_post.append(blend_handler)
    bpy.app.handlers.load_post.append(afk_handler)
    # bpy.app.handlers.load_post.append(event_handler)
    bpy.app.handlers.save_post.append(save_handler)


def unregister():
    bpy.app.handlers.save_post.remove(save_handler)
    # bpy.app.handlers.load_post.remove(event_handler)
    bpy.app.handlers.load_post.remove(afk_handler)
    bpy.app.handlers.load_post.remove(blend_handler)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
