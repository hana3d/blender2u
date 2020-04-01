import bpy


class S3Download(bpy.types.Operator):
    """S3 Download"""
    bl_idname = "matlib.s3_download"
    bl_label = "S3 Download"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}


class S3Upload(bpy.types.Operator):
    """S3 Upload"""
    bl_idname = "matlib.s3_upload"
    bl_label = "S3 Upload"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}
