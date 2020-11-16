import bpy
import os
import requests
import shutil
import urllib.request
from .materials_library_vx import refresh_libs

# api_url = "http://localhost:4000"
api_url = "https://dev-api.r2u.io/blender"

matlib_path = os.path.dirname(__file__)


class S3Download(bpy.types.Operator):
    """S3 Download"""
    bl_idname = "matlib.s3_download"
    bl_label = "S3 Download"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        data = requests.get(url=(api_url + '/matlib-get'))
        for lib in data.json():
            print(lib)
            key = lib['key'].replace('matlib/', '')
            url = lib['url']
            with urllib.request.urlopen(url) as response, open(matlib_path + os.sep + key, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

        refresh_libs()

        return {'FINISHED'}


class S3Upload(bpy.types.Operator):
    """S3 Upload"""
    bl_idname = "matlib.s3_upload"
    bl_label = "S3 Upload"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        library_name = context.scene.matlib.current_library.name
        data = {
            'filename': library_name
        }

        r = requests.post(url=(api_url + '/matlib-post'), json=data)
        response = r.json()
        object_name = matlib_path + os.sep + library_name
        with open(object_name, 'rb') as f:
            files = {'file': (object_name, f)}
            http_response = requests.post(response['url'], data=response['fields'], files=files)
            print(http_response)

        return {'FINISHED'}
