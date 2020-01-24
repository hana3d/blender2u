import bpy
import datetime
import getpass
import uuid


version = '1.1'
api_url = "https://api.real2u.com.br/blender/analytics"
# api_url = "http://localhost:4000/blender/analytics"
user = getpass.getuser()
session_id = str(uuid.uuid1())


def get_blend_file():
    return bpy.path.basename(bpy.context.blend_data.filepath)


def get_blender_version():
    return bpy.app.version_string


def get_collections():
    return len(bpy.data.collections)


def get_objects():
    return len(bpy.data.collections)


def get_timestamp():
    return datetime.datetime.now().isoformat()


def get_uuid():
    return str(uuid.uuid1())
