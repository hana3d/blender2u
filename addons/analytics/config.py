import bpy
import datetime
import getpass
import uuid

version = '1.0'
api_url = "https://api.real2u.com.br/blender/analytics"
# blend_file = bpy.path.basename(bpy.context.blend_data.filepath)
event_id = str(uuid.uuid1())
timestamp = datetime.datetime.now().isoformat()
user = getpass.getuser()
