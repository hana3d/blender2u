import bpy
import pathlib


class MultipleMaterials(bpy.types.Operator):
    """Import multiple materials from a input folder"""
    bl_idname = "material.multiple_import"
    bl_label = "Import Material"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty()

    def execute(self, context):
        path = self.directory

        for filepath in pathlib.Path(path).iterdir():
            bpy.ops.material.single_import('EXEC_DEFAULT', filepath=str(filepath))

        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except:
            print('Addon analytics not installed')

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}
