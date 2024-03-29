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
    "name": "glb-export",
    "author": "R2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Import-Export"
}

import bpy
from mathutils import Vector
# from .bake_nodes import bake_nodes
from .warning import check_file
from .panel import OBJECT_PT_GLBExportPanel


class GLBExport(bpy.types.Operator):
    """GLB Export"""
    bl_idname = "export_scene.glb_export"
    bl_label = "GLB Export"
    bl_options = {'REGISTER', 'UNDO'}

    # Define this to tell 'fileselect_add' that we want a directoy
    directory: bpy.props.StringProperty(
        name="Outdir Path",
        description="Where I will save my stuff"
        # subtype='DIR_PATH' is not needed to specify the selection mode.
        # But this will be anyway a directory path.
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
        context.view_layer.active_layer_collection = context.scene.view_layers[0].layer_collection

        path = self.directory

        try:
            bpy.ops.object.select_all(action='SELECT')
            print('select')
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            print('clear parent')
            bpy.ops.object.select_by_type(extend=False, type='EMPTY')
            print('select empty')
            bpy.ops.object.delete(use_global=True, confirm=False)
        except:
            print('No empties')

        collections = bpy.data.collections

        bpy.ops.object.select_all(action='DESELECT')
        for coll in collections:
            layer = context.view_layer.layer_collection

            coll_layer = layer.children.get(coll.name)
            if coll_layer is None:
                coll_layer = self.find_layer_collection(layer, coll.name)

            if coll.hide_viewport is True or coll_layer.hide_viewport is True:
                continue

            min_x = 999999
            min_y = 999999
            max_x = -999999
            max_y = -999999

            valid_object = False

            for obj in coll.objects:
                if (obj.visible_get()):
                    valid_object = True
                    obj.select_set(True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=False)

                    # bake_nodes(obj)

                    for vertex in [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]:
                        min_x = (min_x, vertex[0])[vertex[0] < min_x]
                        min_y = (min_y, vertex[1])[vertex[1] < min_y]
                        # min_z = (min_z, vertex[2])[vertex[2] < min_z]
                        max_x = (max_x, vertex[0])[vertex[0] > max_x]
                        max_y = (max_y, vertex[1])[vertex[1] > max_y]
                        # max_z = (max_z, vertex[2])[vertex[2] > max_z]

                    bpy.ops.object.select_all(action='DESELECT')

            if not valid_object:
                continue

            center_x = min_x + (max_x - min_x) / 2
            center_y = min_y + (max_y - min_y) / 2
            bpy.ops.object.add(type='EMPTY', location=(center_x, center_y, 0.0))
            empty = bpy.context.selected_objects[0]
            coll.objects.link(empty)
            bpy.context.view_layer.active_layer_collection.collection.objects.unlink(empty)

            bpy.context.view_layer.objects.active = empty

            bpy.ops.object.select_all(action='DESELECT')
            for obj in coll.objects:
                if obj != empty:
                    if (obj.visible_get()):
                        obj.select_set(True)

            bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
            bpy.ops.object.select_all(action='DESELECT')
            empty.select_set(True)

            location = empty.location.copy()
            empty.location.x = 0
            empty.location.y = 0
            for select in coll.objects:
                if (select.visible_get()):
                    select.select_set(True)
            filename = path + coll.name + '.glb'
            bpy.ops.export_scene.gltf(export_image_format='JPEG', filepath=filename, export_selected=True, export_apply=True)
            empty.location = location

            check_file(self, context, filename, coll.name)

            bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.select_by_type(extend=False, type='EMPTY')
        bpy.ops.object.delete(use_global=True, confirm=False)
        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except:
            print('Addon analytics not installed')
        # Open browser, take reference to 'self' read the path to selected
        # file, put path in predetermined self fields.
        # See: https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        context.window_manager.fileselect_add(self)
        # Tells Blender to hang on for the slow user input
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    self.layout.operator(GLBExport.bl_idname)


classes = (
    GLBExport,
    OBJECT_PT_GLBExportPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # bpy.types.TOPBAR_MT_file_export.remove(menu_func)


if __name__ == "__main__":
    register()
