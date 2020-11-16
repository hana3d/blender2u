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
from .panel import OBJECT_PT_UVPanel
from .color import ApplyUVTexture, RemoveUVTexture


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


def register():
    bpy.utils.register_class(FacesArray)
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
    bpy.utils.unregister_class(FacesArray)


if __name__ == "__main__":
    register()
