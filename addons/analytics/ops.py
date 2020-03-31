import bpy
import requests
from .config import api_url, ops_message


class OpsAnalytics(bpy.types.Operator):
    """Send called operator usage to S3 analytics"""
    bl_idname = "script.ops_analytics"
    bl_label = "Operator Analytics"

    operator_name: bpy.props.StringProperty()

    def execute(self, context):
        data = ops_message(self.operator_name)
        r = requests.post(url=api_url, json=data)
        print(r.status_code)
        return {'FINISHED'}
