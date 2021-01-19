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
    "author": "R2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Material"
}

import bpy

from .operators import (
    ApplyUVTextureAll,
    ApplyUVTextureSelected,
    RemoveUVTexture
)
from .panel import OBJECT_PT_UVPanel


class FacesArray(bpy.types.PropertyGroup):
    face: bpy.props.IntProperty()

    def add_face(self, ob):
        self.face = ob
        return self.face


class MaterialArray(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(type=bpy.types.Material)
    faces: bpy.props.CollectionProperty(type=FacesArray)

    def add_material(self, ob):
        self.material = ob
        return self.material

    def add_face(self, ob):
        self.faces.add().add_face(ob)
        return self.faces


classes = (
    FacesArray,
    MaterialArray,
    ApplyUVTextureAll,
    ApplyUVTextureSelected,
    RemoveUVTexture,
    OBJECT_PT_UVPanel,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)

    bpy.types.Object.original_material = bpy.props.CollectionProperty(type=MaterialArray)


def unregister():
    if hasattr(bpy.types.Object, 'original_material'):
        del(bpy.types.Object.original_material)

    for class_ in reversed(classes):
        bpy.utils.unregister_class(class_)


if __name__ == "__main__":
    register()
