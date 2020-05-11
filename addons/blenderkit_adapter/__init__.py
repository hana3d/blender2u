bl_info = {
    "name": "BlenderKit Adapter",
    "author": "real2U",
    "version": (0, 1, 0),
    "blender": (2, 82, 0),
    "category": "3D View",
}

import os

import bpy
import blenderkit


get_bkit_url = blenderkit.paths.get_bkit_url

URL_3D_KIT_MAIN = 'http://3.211.165.243:8080'
URL_3D_KIT_LOCAL = 'http://localhost:8080'
URL_3D_KIT_DEV = os.getenv('URL_3D_KIT_DEV')


def get_bkit_url2():
    if bpy.app.debug_value == 1:
        return URL_3D_KIT_LOCAL

    if bpy.app.debug_value == 2:
        assert URL_3D_KIT_DEV is not None, f'Environment variable URL_3D_KIT_DEV not found'
        return URL_3D_KIT_DEV

    return URL_3D_KIT_MAIN


def register():
    blenderkit.paths.get_bkit_url = get_bkit_url2


def unregister():
    blenderkit.paths.get_bkit_url = get_bkit_url
