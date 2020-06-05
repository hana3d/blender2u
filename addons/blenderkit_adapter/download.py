import os
import shutil

import bpy
import blenderkit
from blenderkit import paths, append_link


append_asset = blenderkit.download.append_asset
append_objects = blenderkit.append_link.append_objects


def selection_get():
    aob = bpy.context.view_layer.objects.active
    selobs = bpy.context.view_layer.objects.selected[:]
    return (aob, selobs)


def selection_set(sel):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = sel[0]
    for ob in sel[1]:
        ob.select_set(True)


def append_objects2(file_name, obnames=[], location=(0, 0, 0), link=False, **kwargs):
    '''append objects into scene individually'''

    with bpy.data.libraries.load(file_name, link=link, relative=True) as (data_from, data_to):
        sobs = []
        for ob in data_from.objects:
            if ob in obnames or obnames == []:
                sobs.append(ob)
        data_to.objects = sobs

    sel = selection_get()
    bpy.ops.object.select_all(action='DESELECT')

    return_obs = []
    main_object = None
    hidden_objects = []

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.view_layer.active_layer_collection.collection.objects.link(obj)
            if obj.parent is None:
                obj.location = location
                main_object = obj
            obj.select_set(True)
            if link is True:
                if obj.hide_viewport:
                    hidden_objects.append(obj)
                    obj.hide_viewport = False
            return_obs.append(obj)
    if link is True:
        bpy.ops.object.make_local(type='SELECT_OBJECT')
        for ob in hidden_objects:
            ob.hide_viewport = True

    if kwargs.get('rotation') is not None:
        main_object.rotation_euler = kwargs['rotation']

    if kwargs.get('parent') is not None:
        main_object.parent = bpy.data.objects[kwargs['parent']]
        main_object.matrix_world.translation = location

    bpy.ops.object.select_all(action='DESELECT')

    selection_set(sel)

    return main_object, return_obs


def asset_in_scene(asset_data):
    '''checks if the asset is already in scene. If yes, modifies asset data so the asset can be reached again.'''
    scene = bpy.context.scene
    au = scene.get('assets used', {})

    id = asset_data['asset_base_id']
    if id in au.keys():
        ad = au[id]
        if ad.get('file_name') is not None:

            asset_data['file_name'] = ad['file_name']
            asset_data['url'] = ad['url']

            c = bpy.data.collections.get(ad['name'])
            if c is not None:
                if c.users > 0:
                    return 'LINKED'
            return 'APPENDED'
    return False


def append_asset2(asset_data, **kwargs):
    '''Link asset to the scene'''

    file_names = paths.get_download_filenames(asset_data)
    scene = bpy.context.scene

    user_preferences = bpy.context.preferences.addons['blenderkit'].preferences

    if user_preferences.api_key == '':
        user_preferences.asset_counter += 1

    if asset_data['asset_type'] == 'scene':
        scene = append_link.append_scene(file_names[0], link=False, fake_user=False)
        parent = scene

    if asset_data['asset_type'] == 'model':
        s = bpy.context.scene
        downloaders = kwargs.get('downloaders')
        s = bpy.context.scene
        sprops = s.blenderkit_models
        if sprops.append_method == 'LINK_COLLECTION':
            sprops.append_link = 'LINK'
            sprops.import_as = 'GROUP'
        else:
            sprops.append_link = 'APPEND'
            sprops.import_as = 'INDIVIDUAL'

        al = sprops.append_link
        ain = asset_in_scene(asset_data)
        if ain is not False:
            if ain == 'LINKED':
                al = 'LINK'
            else:
                al = 'APPEND'

        link = al == 'LINK'
        if downloaders:
            for downloader in downloaders:
                if link is True:
                    parent, newobs = append_link.link_collection(
                        file_names[-1],
                        location=downloader['location'],
                        rotation=downloader['rotation'],
                        link=link,
                        name=asset_data['name'],
                        parent=kwargs.get('parent'))
                else:
                    parent, newobs = append_link.append_objects(
                        file_names[-1],
                        location=downloader['location'],
                        rotation=downloader['rotation'],
                        link=link,
                        name=asset_data['name'],
                        parent=kwargs.get('parent'))

                if parent.type == 'EMPTY' and link:
                    bmin = asset_data['bbox_min']
                    bmax = asset_data['bbox_max']
                    size_min = min(1.0, (bmax[0] - bmin[0] + bmax[1] - bmin[1] + bmax[2] - bmin[2]) / 3)
                    parent.empty_display_size = size_min

        elif kwargs.get('model_location') is not None:
            if link is True:
                parent, newobs = append_link.link_collection(
                    file_names[-1],
                    location=kwargs['model_location'],
                    rotation=kwargs['model_rotation'],
                    link=link,
                    name=asset_data['name'],
                    parent=kwargs.get('parent'))
            else:
                parent, newobs = append_link.append_objects(
                    file_names[-1],
                    location=kwargs['model_location'],
                    rotation=kwargs['model_rotation'],
                    link=link,
                    parent=kwargs.get('parent'))
            if parent.type == 'EMPTY' and link:
                bmin = asset_data['bbox_min']
                bmax = asset_data['bbox_max']
                size_min = min(1.0, (bmax[0] - bmin[0] + bmax[1] - bmin[1] + bmax[2] - bmin[2]) / 3)
                parent.empty_display_size = size_min

        if link:
            group = parent.instance_collection

            lib = group.library
            lib['asset_data'] = asset_data

    elif asset_data['asset_type'] == 'brush':

        inscene = False
        for b in bpy.data.brushes:
            if b.blenderkit.id == asset_data['id']:
                inscene = True
                brush = b
                break
        if not inscene:
            brush = append_link.append_brush(file_names[-1], link=False, fake_user=False)

            thumbnail_name = asset_data['thumbnail'].split(os.sep)[-1]
            tempdir = paths.get_temp_dir('brush_search')
            thumbpath = os.path.join(tempdir, thumbnail_name)
            asset_thumbs_dir = paths.get_download_dirs('brush')[0]
            asset_thumb_path = os.path.join(asset_thumbs_dir, thumbnail_name)
            shutil.copy(thumbpath, asset_thumb_path)
            brush.icon_filepath = asset_thumb_path

        if bpy.context.view_layer.objects.active.mode == 'SCULPT':
            bpy.context.tool_settings.sculpt.brush = brush
        elif bpy.context.view_layer.objects.active.mode == 'TEXTURE_PAINT':
            bpy.context.tool_settings.image_paint.brush = brush

        parent = brush

    elif asset_data['asset_type'] == 'material':
        inscene = False
        for m in bpy.data.materials:
            if m.blenderkit.id == asset_data['id']:
                inscene = True
                material = m
                break
        if not inscene:
            material = append_link.append_material(file_names[-1], link=False, fake_user=False)
        target_object = bpy.data.objects[kwargs['target_object']]

        if len(target_object.material_slots) == 0:
            target_object.data.materials.append(material)
        else:
            target_object.material_slots[kwargs['material_target_slot']].material = material

        parent = material

    scene['assets used'] = scene.get('assets used', {})
    scene['assets used'][asset_data['asset_base_id']] = asset_data.copy()

    scene['assets rated'] = scene.get('assets rated', {})

    id = asset_data['asset_base_id']
    scene['assets rated'][id] = scene['assets rated'].get(id, False)

    parent['asset_data'] = asset_data

    if hasattr(parent.blenderkit, 'tags') and 'tags' in asset_data:
        asset_data['tags'].remove('non-manifold')
        parent.blenderkit.tags = ','.join(asset_data['tags'])
    if hasattr(parent.blenderkit, 'description') and 'description' in asset_data:
        if asset_data['description'] is not None:
            parent.blenderkit.description = asset_data['description']
    if hasattr(parent.blenderkit, 'custom_props') and 'metadata' in asset_data:
        if 'product_info' in asset_data['metadata']:
            product_info = asset_data['metadata'].pop('product_info')
            clients = []
            skus = []
            for client_sku in product_info:
                clients.append(client_sku['client'])
                skus.append(client_sku['sku'])
            if hasattr(parent.blenderkit, 'client') and hasattr(parent.blenderkit, 'sku'):
                parent.blenderkit.client = ','.join(clients)
                parent.blenderkit.sku = ','.join(skus)
            else:
                parent.blenderkit.custom_props['client'] = ','.join(clients)
                parent.blenderkit.custom_props['sku'] = ','.join(skus)

        for key, value in asset_data['metadata'].items():
            parent.blenderkit.custom_props[key] = value

    bpy.ops.wm.undo_push_context(message='add %s to scene' % asset_data['name'])


def register():
    blenderkit.append_link.append_objects = append_objects2
    blenderkit.download.append_asset = append_asset2


def unregister():
    blenderkit.download.append_asset = append_asset
    blenderkit.append_link.append_objects = append_objects
