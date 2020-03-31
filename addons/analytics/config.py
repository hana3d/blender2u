import bpy
import datetime
import getpass
import uuid


version = '1.2'
api_url = "https://api.real2u.com.br/blender/analytics"
# api_url = "http://localhost:4000/blender/analytics"
user = getpass.getuser()
session_id = str(uuid.uuid1())
is_afk = 1


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


def basic_message():
    data = {
        'blend': get_blend_file(),
        'blender_version': get_blender_version(),
        'collections_count': get_collections(),
        'event_id': get_uuid(),
        'objects_count': get_objects(),
        'session_id': session_id,
        'timestamp': get_timestamp(),
        'user': user,
        'version': version
    }
    return data


def ops_message(operator_name):
    data = {
        'addon': operator_name,
        'session_id': session_id,
        'timestamp': get_timestamp(),
        'user': user,
        'version': version
    }
    return data
