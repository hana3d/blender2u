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
    "name": "polycount-manager",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "version": (1, 6, 0),
    "location": "",
    "warning": "",
    "category": "Mesh"
}

import bpy
from .collections import count_collections
from .objects import count_objects
from .panel import OBJECT_PT_PolycountPanel
from .color import ColorObjects, OriginalColor


class PolycountCollections(bpy.types.Operator):
    """Polycount Collections"""
    bl_idname = "object.polycount_collections"
    bl_label = "Polycount Collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count_collections()

        return {'FINISHED'}


class PolycountObjects(bpy.types.Operator):
    """Polycount Objects"""
    bl_idname = "object.polycount_objects"
    bl_label = "Polycount Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count_objects()

        return {'FINISHED'}


class MaterialArray(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(type=bpy.types.Material)

    def add(self, ob):
        self.material = ob
        return self.material


def menu_func(self, context):
    self.layout.operator(PolycountCollections.bl_idname)
    self.layout.operator(PolycountObjects.bl_idname)


def register():
    bpy.utils.register_class(MaterialArray)
    bpy.types.Object.original_material = bpy.props.CollectionProperty(type=MaterialArray)

    bpy.utils.register_class(PolycountCollections)
    bpy.utils.register_class(PolycountObjects)
    bpy.utils.register_class(OBJECT_PT_PolycountPanel)
    bpy.utils.register_class(ColorObjects)
    bpy.utils.register_class(OriginalColor)
    # bpy.types.TOPBAR_MT_edit.append(menu_func)


def unregister():
    # bpy.types.TOPBAR_MT_edit.remove(menu_func)
    bpy.utils.unregister_class(OriginalColor)
    bpy.utils.unregister_class(ColorObjects)
    bpy.utils.unregister_class(OBJECT_PT_PolycountPanel)
    bpy.utils.unregister_class(PolycountObjects)
    bpy.utils.unregister_class(PolycountCollections)

    del(bpy.types.Object.original_material)
    bpy.utils.unregister_class(MaterialArray)


if __name__ == "__main__":
    register()
