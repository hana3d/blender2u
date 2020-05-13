bl_info = {
    "name": "BlenderKit Adapter",
    "author": "real2U",
    "version": (0, 1, 0),
    "blender": (2, 82, 0),
    "category": "3D View",
}

import os
import copy

import bpy
import blenderkit


get_bkit_url = blenderkit.paths.get_bkit_url
model_search_config = blenderkit.BlenderKitModelSearchProps.__annotations__

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


def change_default_append():
    model_search_config2 = copy.deepcopy(model_search_config)

    model_search_config2['append_method'][1]['default'] = 'APPEND_OBJECTS'
    model_search_config2['append_link'][1]['default'] = 'APPEND'

    blenderkit.BlenderKitModelSearchProps.__annotations__ = model_search_config2

    bpy.utils.unregister_class(blenderkit.BlenderKitModelSearchProps)
    bpy.utils.register_class(blenderkit.BlenderKitModelSearchProps)

    bpy.types.Scene.blenderkit_models = bpy.props.PointerProperty(
        type=blenderkit.BlenderKitModelSearchProps)


def restore_default_append():
    blenderkit.BlenderKitModelSearchProps.__annotations__ = model_search_config

    bpy.utils.unregister_class(blenderkit.BlenderKitModelSearchProps)
    bpy.utils.register_class(blenderkit.BlenderKitModelSearchProps)

    bpy.types.Scene.blenderkit_models = bpy.props.PointerProperty(
        type=blenderkit.BlenderKitModelSearchProps)


def register():
    blenderkit.paths.get_bkit_url = get_bkit_url2
    if getattr(blenderkit.BlenderKitModelSearchProps, "is_registered"):
        change_default_append()


def unregister():
    blenderkit.paths.get_bkit_url = get_bkit_url
    if getattr(blenderkit.BlenderKitModelSearchProps, "is_registered"):
        restore_default_append()
