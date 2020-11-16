bl_info = {
    "name": "BlenderKit Adapter",
    "author": "R2U",
    "version": (0, 1, 0),
    "blender": (2, 82, 0),
    "category": "3D View",
}

import os

import bpy
import blenderkit

from . import annotations, ui, ui_scene, custom_props, download, search


get_bkit_url = blenderkit.paths.get_bkit_url
get_upload_data = blenderkit.upload.get_upload_data
model_search_config = blenderkit.BlenderKitModelSearchProps.__annotations__
material_search_config = blenderkit.BlenderKitMaterialSearchProps.__annotations__
model_upload_props = blenderkit.BlenderKitModelUploadProps.__annotations__
material_upload_props = blenderkit.BlenderKitMaterialUploadProps.__annotations__
upload_operator = blenderkit.upload.UploadOperator.__annotations__

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


def get_upload_data2(self, context, asset_type):
    export_data, upload_data, eval_path_computing, eval_path_state, eval_path, props = get_upload_data(self, context,
                                                                                                       asset_type)

    if hasattr(props, 'client'):
        upload_data['client'] = props.client
    if hasattr(props, 'sku'):
        upload_data['sku'] = props.sku
    if hasattr(props, 'custom_props'):
        upload_data['metadata'] = {}
        for key in props.custom_props.keys():
            upload_data['metadata'][key] = props.custom_props[key]

    return export_data, upload_data, eval_path_computing, eval_path_state, eval_path, props


def change_default_append(annotations):
    annotations['append_method'][1]['default'] = 'APPEND_OBJECTS'
    annotations['append_link'][1]['default'] = 'APPEND'


def create_custom_props(annotations):
    annotations['client'] = bpy.props.StringProperty(name="Client")
    annotations['sku'] = bpy.props.StringProperty(name="SKU")
    annotations['custom_props'] = bpy.props.PointerProperty(type=custom_props.CustomPropsPropertyGroup)


def change_default_automap(annotations):
    annotations['automap'][1]['default'] = False


def register():
    custom_props.register()
    blenderkit.paths.get_bkit_url = get_bkit_url2
    blenderkit.upload.get_upload_data = get_upload_data2
    annotations.change_annotations(
        blenderkit.BlenderKitModelSearchProps,
        model_search_config,
        change_default_append,
        'bpy.types.Scene.blenderkit_models'
    )
    annotations.change_annotations(
        blenderkit.BlenderKitModelUploadProps,
        model_upload_props,
        create_custom_props,
        'bpy.types.Object.blenderkit'
    )
    annotations.change_annotations(
        blenderkit.BlenderKitMaterialUploadProps,
        material_upload_props,
        create_custom_props,
        'bpy.types.Material.blenderkit'
    )
    annotations.change_annotations(
        blenderkit.BlenderKitMaterialSearchProps,
        material_search_config,
        change_default_automap,
        'bpy.types.Scene.blenderkit_mat'
    )

    search.register()
    download.register()
    ui.register()
    ui_scene.register()


def unregister():
    ui_scene.unregister()
    ui.unregister()
    annotations.restore_annotations(
        blenderkit.BlenderKitMaterialSearchProps,
        material_search_config,
        'bpy.types.Scene.blenderkit_mat'
    )
    annotations.restore_annotations(
        blenderkit.BlenderKitMaterialUploadProps,
        material_upload_props,
        'bpy.types.Material.blenderkit')
    annotations.restore_annotations(
        blenderkit.BlenderKitModelUploadProps,
        model_upload_props,
        'bpy.types.Object.blenderkit')
    annotations.restore_annotations(
        blenderkit.BlenderKitModelSearchProps,
        model_search_config,
        'bpy.types.Scene.blenderkit_models')
    download.unregister()
    search.unregister()
    blenderkit.upload.get_upload_data = get_upload_data
    blenderkit.paths.get_bkit_url = get_bkit_url
    custom_props.unregister()
