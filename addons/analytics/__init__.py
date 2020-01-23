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
import os
from .blend import blend_handler, BlendModal
# from .events import event_handler, EventModal
# from .reports import report_handler, ReportModal


def register():
    bpy.utils.register_class(BlendModal)
    # bpy.utils.register_class(EventModal)
    # bpy.utils.register_class(ReportModal)
    bpy.app.handlers.load_post.append(blend_handler)
    # bpy.app.handlers.load_post.append(event_handler)


def unregister():
    # bpy.app.handlers.load_post.remove(event_handler)
    bpy.app.handlers.load_post.remove(blend_handler)
    # bpy.utils.unregister_class(ReportModal)
    # bpy.utils.unregister_class(EventModal)
    bpy.utils.unregister_class(BlendModal)


if __name__ == "__main__":
    register()
