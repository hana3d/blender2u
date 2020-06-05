import os
import random
import json

import bpy
import blenderkit

from blenderkit import colors, paths, tasks_queue, ui, utils, search


timer_update = blenderkit.search.timer_update


@bpy.app.handlers.persistent
def timer_update2():
    preferences = bpy.context.preferences.addons['blenderkit'].preferences
    if search.first_time:
        search.first_time = False
        if preferences.show_on_start:
            search()
        if preferences.tips_on_start:
            ui.get_largest_3dview()
            ui.update_ui_size(ui.active_area, ui.active_region)
            ui.add_report(text='BlenderKit Tip: ' + random.choice(search.rtips), timeout=12, color=colors.GREEN)

    if bpy.context.window_manager.clipboard != search.last_clipboard:
        last_clipboard = bpy.context.window_manager.clipboard
        instr = 'asset_base_id:'
        if last_clipboard[:len(instr)] == instr:
            atstr = 'asset_type:'
            ati = last_clipboard.find(atstr)
            if ati > -1:
                search_props = utils.get_search_props()
                search_props.search_keywords = last_clipboard

    if len(search.search_threads) == 0 or bpy.context.scene.blenderkitUI.dragging:
        return 1
    for thread in search.search_threads:
        if not thread[0].is_alive():
            search.search_threads.remove(thread)  #
            icons_dir = thread[1]
            scene = bpy.context.scene
            s = bpy.context.scene
            asset_type = thread[2]
            if asset_type == 'model':
                props = scene.blenderkit_models
                json_filepath = os.path.join(icons_dir, 'model_searchresult.json')
                search_name = 'bkit model search'
            if asset_type == 'scene':
                props = scene.blenderkit_scene
                json_filepath = os.path.join(icons_dir, 'scene_searchresult.json')
                search_name = 'bkit scene search'
            if asset_type == 'material':
                props = scene.blenderkit_mat
                json_filepath = os.path.join(icons_dir, 'material_searchresult.json')
                search_name = 'bkit material search'
            if asset_type == 'brush':
                props = scene.blenderkit_brush
                json_filepath = os.path.join(icons_dir, 'brush_searchresult.json')
                search_name = 'bkit brush search'

            s[search_name] = []

            if search.reports != '':
                props.report = str(search.reports)
                return .2
            with open(json_filepath, 'r') as data_file:
                rdata = json.load(data_file)

            result_field = []
            ok, error = search.check_errors(rdata)
            if ok:
                bpy.ops.object.run_assetbar_fix_context()
                for r in rdata['results']:
                    try:
                        r['filesSize'] = int(r['filesSize'] / 1024)
                    except:
                        utils.p('asset with no files-size')
                    if r['assetType'] == asset_type:
                        if len(r['files']) > 0:
                            tname = None
                            allthumbs = []
                            durl, tname = None, None
                            for f in r['files']:
                                if f['fileType'] == 'thumbnail':
                                    tname = paths.extract_filename_from_url(f['fileThumbnailLarge'])
                                    small_tname = paths.extract_filename_from_url(f['fileThumbnail'])
                                    allthumbs.append(tname)

                                tdict = {}
                                for i, t in enumerate(allthumbs):
                                    tdict['thumbnail_%i'] = t
                                if f['fileType'] == 'blend':
                                    durl = f['downloadUrl'].split('?')[0]
                            if durl and tname:

                                tooltip = search.generate_tooltip(r)
                                asset_data = {'thumbnail': tname,
                                              'thumbnail_small': small_tname,
                                              'download_url': durl,
                                              'id': r['id'],
                                              'asset_base_id': r['assetBaseId'],
                                              'name': r['name'],
                                              'asset_type': r['assetType'],
                                              'tooltip': tooltip,
                                              'tags': r['tags'],
                                              'can_download': r.get('canDownload', True),
                                              'verification_status': r['verificationStatus'],
                                              'author_id': str(r['author']['id'])
                                              }
                                asset_data['downloaded'] = 0

                                if 'description' in r:
                                    asset_data['description'] = r['description']
                                if 'metadata' in r:
                                    asset_data['metadata'] = r['metadata']
                                if 'sku' in r:
                                    asset_data['sku'] = r['sku']
                                if 'client' in r:
                                    asset_data['client'] = r['client']

                                params = utils.params_to_dict(r['parameters'])

                                if asset_type == 'model':
                                    if params.get('boundBoxMinX') is not None:
                                        bbox = {
                                            'bbox_min': (
                                                float(params['boundBoxMinX']),
                                                float(params['boundBoxMinY']),
                                                float(params['boundBoxMinZ'])),
                                            'bbox_max': (
                                                float(params['boundBoxMaxX']),
                                                float(params['boundBoxMaxY']),
                                                float(params['boundBoxMaxZ']))
                                        }

                                    else:
                                        bbox = {
                                            'bbox_min': (-.5, -.5, 0),
                                            'bbox_max': (.5, .5, 1)
                                        }
                                    asset_data.update(bbox)
                                if asset_type == 'material':
                                    asset_data['texture_size_meters'] = params.get('textureSizeMeters', 1.0)

                                asset_data.update(tdict)
                                if r['assetBaseId'] in scene.get('assets used', {}).keys():
                                    asset_data['downloaded'] = 100

                                result_field.append(asset_data)

                s[search_name] = result_field
                s['search results'] = result_field
                s[search_name + ' orig'] = rdata
                s['search results orig'] = rdata
                search.load_previews()
                ui_props = bpy.context.scene.blenderkitUI
                if len(result_field) < ui_props.scrolloffset:
                    ui_props.scrolloffset = 0
                props.is_searching = False
                props.search_error = False
                props.report = 'Found %i results. ' % (s['search results orig']['count'])
                if len(s['search results']) == 0:
                    tasks_queue.add_task((ui.add_report, ('No matching results found.',)))

            else:
                print('error', error)
                props.report = error
                props.search_error = True

            search.mt('preview loading finished')
    return .3


def register():
    if bpy.app.timers.is_registered(blenderkit.search.timer_update):
        bpy.app.timers.unregister(blenderkit.search.timer_update)
    blenderkit.search.timer_update = timer_update2
    bpy.app.timers.register(blenderkit.search.timer_update, persistent=True)


def unregister():
    if bpy.app.timers.is_registered(blenderkit.search.timer_update):
        bpy.app.timers.unregister(blenderkit.search.timer_update)
    blenderkit.search.timer_update = timer_update
    bpy.app.timers.register(blenderkit.search.timer_update, persistent=True)
