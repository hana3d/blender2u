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
    "name": "glb-import",
    "author": "R2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Import-Export"
}

import bpy
import pathlib
from .panel import OBJECT_PT_GLBImportPanel


class GLBImport(bpy.types.Operator):
    """GLB Import"""
    bl_idname = "import_scene.glb_import"
    bl_label = "Choose Folder"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty(
        name="Input Path",
        description="Where to find stuff",
        subtype='DIR_PATH'
    )

    filter_glob: bpy.props.StringProperty(
        default='*.glb, *.gltf',
        options={'HIDDEN'}
    )

    def find_layer_collection(self, parent_layer, coll_name):
        for child in parent_layer.children:
            layer = child.children.get(coll_name)
            if layer is not None:
                return layer
            else:
                layer = self.find_layer_collection(child, coll_name)
                if layer is not None:
                    return layer
        return None

    def execute(self, context):
        path = bpy.path.abspath(self.directory)

        for file in pathlib.Path(path).iterdir():
            if(file.suffix != '.glb'):
                continue
            bpy.ops.import_scene.gltf(filepath=str(file))
            imported = context.selected_objects[:]
            collection = bpy.data.collections.new(file.stem)
            context.scene.collection.children.link(collection)
            for ob in imported:
                collection.objects.link(ob)
            for ob in context.scene.collection.objects:
                context.scene.collection.objects.unlink(ob)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


classes = (
    GLBImport,
    OBJECT_PT_GLBImportPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
