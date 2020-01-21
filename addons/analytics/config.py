import bpy
import datetime
import getpass


version = '1.0'
api_url = "https://api.real2u.com.br/blender/analytics"
# api_url = "http://localhost:4000/blender/analytics"
# blend_file = bpy.path.basename(bpy.context.blend_data.filepath)
timestamp = datetime.datetime.now().isoformat()
user = getpass.getuser()
