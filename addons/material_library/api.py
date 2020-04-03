import bpy
import os
import requests
import shutil
import urllib.request
from .materials_library_vx import refresh_libs

api_url = "http://localhost:4000"
# api_url = "https://staging-api.real2u.com.br/blender"

matlib_path = os.path.dirname(__file__)


class S3Download(bpy.types.Operator):
    """S3 Download"""
    bl_idname = "matlib.s3_download"
    bl_label = "S3 Download"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        signed_url_request = requests.get(url=(api_url + '/matlib-get'))
        with urllib.request.urlopen(signed_url_request.json()) as response, open(matlib_path + os.sep + 'cycles_materials.blend', 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        refresh_libs()

        return {'FINISHED'}


class S3Upload(bpy.types.Operator):
    """S3 Upload"""
    bl_idname = "matlib.s3_upload"
    bl_label = "S3 Upload"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}
