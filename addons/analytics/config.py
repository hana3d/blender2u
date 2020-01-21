import bpy
import datetime
import getpass
import uuid

version = '0.1'
api_url = "https://api.real2u.com.br/blender"
blend_file = bpy.path.basename(bpy.context.blend_data.filepath)
event_id = uuid.uuid1()
timestamp = datetime.datetime.now().isoformat()
user = getpass.getuser()
