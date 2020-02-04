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
    "name": "uv-check",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Material"
}

import bpy
from .panel import OBJECT_PT_UVPanel
from .color import ApplyUVTexture, RemoveUVTexture


class MaterialArray(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(type=bpy.types.Material)

    def add(self, ob):
        self.material = ob
        return self.material


def register():
    bpy.utils.register_class(MaterialArray)
    bpy.types.Object.original_material = bpy.props.CollectionProperty(type=MaterialArray)

    bpy.utils.register_class(OBJECT_PT_UVPanel)
    bpy.utils.register_class(ApplyUVTexture)
    bpy.utils.register_class(RemoveUVTexture)


def unregister():
    bpy.utils.unregister_class(RemoveUVTexture)
    bpy.utils.unregister_class(ApplyUVTexture)
    bpy.utils.unregister_class(OBJECT_PT_UVPanel)

    if hasattr(bpy.types.Object, 'original_material'):
        del(bpy.types.Object.original_material)
    bpy.utils.unregister_class(MaterialArray)


if __name__ == "__main__":
    register()
