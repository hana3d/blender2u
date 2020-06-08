import os
import sys

import bpy
import blenderkit

from . import annotations, render_settings


blenderkit_ui_props = blenderkit.BlenderKitUIProps.__annotations__
scene_upload_props = blenderkit.BlenderKitSceneUploadProps.__annotations__
scene_search_props = blenderkit.BlenderKitSceneSearchProps.__annotations__
get_missing_data_scene = blenderkit.upload.get_missing_data_scene
modal = blenderkit.ui.AssetBarOperator.modal
try_finished_append = blenderkit.download.try_finished_append
draw_panel_scene_search = blenderkit.ui_panels.draw_panel_scene_search
append_scene = blenderkit.append_link.append_scene


def asset_type_callback2(self, context):
    if self.down_up == 'SEARCH':
        items = (
            ('MODEL', 'Find Models', 'Find models in the 3DKit online database', 'OBJECT_DATAMODE', 0),
            ('SCENE', 'Find Scenes', 'Find scenes in the 3DKit online database', 'SCENE_DATA', 1),
            ('MATERIAL', 'Find Materials', 'Find materials in the 3DKit online database', 'MATERIAL', 2),
            # ('HDR', 'Find HDRs', 'Find HDRs in the 3DKit online database', 'WORLD_DATA', 3),
        )
    else:
        items = (
            ('MODEL', 'Upload Model', 'Upload a model to 3DKit', 'OBJECT_DATAMODE', 0),
            ('SCENE', 'Upload Scene', 'Upload a scene to 3DKit', 'SCENE_DATA', 1),
            ('MATERIAL', 'Upload Material', 'Upload a material to 3DKit', 'MATERIAL', 2),
            # ('HDR', 'Upload HDR', 'Upload a HDR to 3DKit', 'WORLD_DATA', 3),
        )
    return items


def switch_search_results2(self, context):
    s = bpy.context.scene
    props = s.blenderkitUI
    if props.asset_type == 'MODEL':
        s['search results'] = s.get('bkit model search')
        s['search results orig'] = s.get('bkit model search orig')
    elif props.asset_type == 'SCENE':
        s['search results'] = s.get('bkit scene search')
        s['search results orig'] = s.get('bkit scene search orig')
    elif props.asset_type == 'MATERIAL':
        s['search results'] = s.get('bkit material search')
        s['search results orig'] = s.get('bkit material search orig')
    elif props.asset_type == 'HDR':
        s['search results'] = s.get('bkit hdr search')
        s['search results orig'] = s.get('bkit hdr search orig')
    blenderkit.search.load_previews()


def change_asset_type(annotations):
    annotations['asset_type'][1]['items'] = asset_type_callback2
    annotations['asset_type'][1]['update'] = switch_search_results2


def change_thumbnail_props(annotations):
    annotations['is_generating_thumbnail'][1]['update'] = blenderkit.autothumb.update_upload_scene_preview
    annotations['thumbnail_denoising'] = bpy.props.BoolProperty(
        name="Use Denoising",
        description="Use denoising",
        default=True
    )
    annotations['thumbnail_resolution'] = bpy.props.EnumProperty(
        name="Resolution",
        items=blenderkit.thumbnail_resolutions,
        description="Thumbnail resolution.",
        default="512",
    )
    annotations['thumbnail_samples'] = bpy.props.IntProperty(
        name="Cycles Samples",
        description="cycles samples setting",
        default=200,
        min=5,
        max=5000
    )
    annotations['category'] = bpy.props.StringProperty(
        name="Category",
        default='',
    )
    annotations['subcategory'] = bpy.props.StringProperty(
        name="Subcategory",
        default='',
    )


def add_scene_search_properties(annotations):
    annotations['merge_add'] = bpy.props.EnumProperty(
        name="How to Attach Scene",
        items=(
            ('MERGE', 'Merge Scenes', ''),
            ('ADD', 'Add New Scene', ''),
        ),
        description="choose if the scene will be merged or appended",
        default="MERGE"
    )

    annotations['import_world'] = bpy.props.BoolProperty(
        name='Import World',
        description="import world data to current scene",
        default=True
    )

    annotations['import_render'] = bpy.props.BoolProperty(
        name='Import Render Settings',
        description="import render settings to current scene",
        default=True
    )


def start_scene_thumbnailer2(self, context):
    # Prepare to save the file
    s = bpy.context.scene
    props = s.blenderkit
    props.is_generating_thumbnail = True
    props.thumbnail_generating_state = 'starting blender instance'

    basename, ext = os.path.splitext(bpy.data.filepath)
    if not basename:
        basename = os.path.join(basename, "temp")
    if not ext:
        ext = ".blend"

    asset_name = os.path.basename(basename)
    file_dir = os.path.dirname(bpy.data.filepath)
    thumb_path = os.path.join(file_dir, asset_name)
    rel_thumb_path = os.path.join('//', asset_name)

    i = 0
    while os.path.isfile(thumb_path + '.png'):
        thumb_path = os.path.join(file_dir, asset_name + '_' + str(i).zfill(4))
        rel_thumb_path = os.path.join('//', asset_name + '_' + str(i).zfill(4))
        i += 1

    try:
        user_preferences = bpy.context.preferences.addons['blenderkit'].preferences

        bpy.context.scene.render.filepath = thumb_path + '.png'
        if user_preferences.thumbnail_use_gpu:
            bpy.context.scene.cycles.device = 'GPU'

        bpy.context.scene.cycles.samples = props.thumbnail_samples
        bpy.context.view_layer.cycles.use_denoising = props.thumbnail_denoising

        x = bpy.context.scene.render.resolution_x
        y = bpy.context.scene.render.resolution_y

        bpy.context.scene.render.resolution_x = int(props.thumbnail_resolution)
        bpy.context.scene.render.resolution_y = int(props.thumbnail_resolution)

        bpy.ops.render.render(write_still=True, animation=False)

        bpy.context.scene.render.resolution_x = x
        bpy.context.scene.render.resolution_y = y

        props.thumbnail = rel_thumb_path + '.png'
        props.thumbnail_generating_state = 'Finished'
        props.is_generating_thumbnail = False

    except Exception as e:
        props.is_generating_thumbnail = False
        self.report({'WARNING'}, "Error while exporting file: %s" % str(e))
        return {'FINISHED'}


class GenerateSceneThumbnailOperator(bpy.types.Operator):
    """Generate Cycles thumbnail for scene"""
    bl_idname = "object.blenderkit_scene_thumbnail"
    bl_label = "BlenderKit Thumbnail Generator"
    bl_options = {'REGISTER', 'INTERNAL'}

    def draw(self, context):
        ob = bpy.context.active_object
        while ob.parent is not None:
            ob = ob.parent
        props = ob.blenderkit
        layout = self.layout
        layout.label(text='thumbnailer settings')
        layout.prop(props, 'thumbnail_samples')
        layout.prop(props, 'thumbnail_resolution')
        layout.prop(props, 'thumbnail_denoising')
        preferences = bpy.context.preferences.addons['blenderkit'].preferences
        layout.prop(preferences, "thumbnail_use_gpu")

    def execute(self, context):
        start_scene_thumbnailer2(self, context)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        if bpy.data.filepath == '':
            title = "Can't render thumbnail"
            message = "please save your file first"

            def draw_message(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw_message, title=title, icon='INFO')
            return {'FINISHED'}

        return wm.invoke_props_dialog(self)


def get_missing_data_scene2(props):
    props.report = ''
    blenderkit.autothumb.update_upload_scene_preview(None, None)

    if props.name == '':
        blenderkit.upload.write_to_report(props, 'Set scene name')
    if not props.has_thumbnail:
        blenderkit.upload.write_to_report(props, 'Add thumbnail:')
        props.report += props.thumbnail_generating_state + '\n'
    if props.engine == 'NONE':
        blenderkit.upload.write_to_report(props, 'Set at least one rendering/output engine')


def modal2(self, context, event):
    ui_props = context.scene.blenderkitUI
    active_index = ui_props.active_index

    if event.value == 'PRESS' and active_index > -1:
        if ui_props.asset_type == 'SCENE':
            context.scene.blenderkitUI.drag_init = True
            bpy.context.window.cursor_set("NONE")
            context.scene.blenderkitUI.draw_tooltip = False
            context.scene.blenderkitUI.drag_length = 0

    modal_answer = modal(self, context, event)

    return modal_answer


def try_finished_append2(asset_data, **kwargs):
    file_names = blenderkit.paths.get_download_filenames(asset_data)
    done = False
    blenderkit.utils.p('try to append already existing asset')
    if len(file_names) > 0:
        if os.path.isfile(file_names[-1]):
            kwargs['name'] = asset_data['name']
            try:
                blenderkit.download.append_asset(asset_data, **kwargs)
                if asset_data['asset_type'] == 'scene':
                    if bpy.context.scene.blenderkit_scene.merge_add == 'ADD':
                        for window in bpy.context.window_manager.windows:
                            window.scene = bpy.data.scenes[asset_data['name']]
                done = True
            except Exception as e:
                print(e)
                for f in file_names:
                    try:
                        os.remove(f)
                    except:
                        e = sys.exc_info()[0]
                        print(e)
                        pass
                done = False
    return done


def draw_panel_scene_search2(self, context):
    s = context.scene
    props = s.blenderkit_scene
    layout = self.layout

    layout.prop(props, "search_keywords", text="", icon='VIEWZOOM')
    layout.prop(props, 'merge_add', expand=True, icon_only=False)

    if props.merge_add == 'MERGE':
        layout.prop(props, 'import_world')
        layout.prop(props, 'import_render')


def append_scene2(file_name, scenename=None, link=False, fake_user=False):
    scene = bpy.context.scene
    props = scene.blenderkit_scene

    if props.merge_add == 'MERGE' and scenename is None:
        with bpy.data.libraries.load(file_name, link=link, relative=True) as (data_from, data_to):
            data_to.collections = [name for name in data_from.collections]
            scene_name = data_from.scenes[0]
            data_to.scenes = [scene_name]

        imported_scene = data_to.scenes[0]
        scene_collection = bpy.data.collections.new(scene_name)
        scene.collection.children.link(scene_collection)
        for col in data_to.collections:
            scene_collection.children.link(col)
        scene.camera = imported_scene.camera
        if props.import_world:
            scene.world = imported_scene.world

        if props.import_render:
            copy_scene_render_attributes(imported_scene, scene, render_settings.SETTINGS)
            if scene.view_settings.use_curve_mapping:
                copy_curves(imported_scene, scene)

        imported_scene.user_clear()
        bpy.data.scenes.remove(imported_scene, do_unlink=False)

        return scene

    return append_scene(file_name, scenename, link, fake_user)


def copy_scene_render_attributes(from_scene, to_scene, settings):
    for attribute in settings:
        from_attribute = getattr(from_scene, attribute)
        to_attribute = getattr(to_scene, attribute)
        for setting in settings[attribute]:
            value = getattr(from_attribute, setting)
            setattr(to_attribute, setting, value)


def copy_curves(from_scene: bpy.types.Scene, to_scene: bpy.types.Scene):
    for curve in to_scene.view_settings.curve_mapping.curves:
        while len(curve.points) > 2:
            curve.points.remove(curve.points[-1])
        curve.points[0].location = (0, 0)
        curve.points[1].location = (1, 1)

    for i, curve in enumerate(from_scene.view_settings.curve_mapping.curves):
        points = to_scene.view_settings.curve_mapping.curves[i].points
        while len(points) < len(curve.points):
            points.new(0, 0)
        for j, point in enumerate(curve.points):
            points[j].location = point.location

    to_scene.view_settings.curve_mapping.black_level = from_scene.view_settings.curve_mapping.black_level
    to_scene.view_settings.curve_mapping.white_level = from_scene.view_settings.curve_mapping.white_level
    to_scene.view_settings.curve_mapping.update()


def register():
    annotations.change_annotations(
        blenderkit.BlenderKitUIProps,
        blenderkit_ui_props,
        change_asset_type,
        'bpy.types.Scene.blenderkitUI'
    )
    annotations.change_annotations(
        blenderkit.BlenderKitSceneUploadProps,
        scene_upload_props,
        change_thumbnail_props,
        'bpy.types.Scene.blenderkit'
    )
    annotations.change_annotations(
        blenderkit.BlenderKitSceneSearchProps,
        scene_search_props,
        add_scene_search_properties,
        'bpy.types.Scene.blenderkit_scene'
    )
    bpy.utils.register_class(GenerateSceneThumbnailOperator)
    blenderkit.upload.get_missing_data_scene = get_missing_data_scene2
    blenderkit.ui.AssetBarOperator.modal = modal2
    blenderkit.download.try_finished_append = try_finished_append2
    blenderkit.ui_panels.draw_panel_scene_search = draw_panel_scene_search2
    blenderkit.append_link.append_scene = append_scene2


def unregister():
    blenderkit.append_link.append_scene = append_scene
    blenderkit.ui_panels.draw_panel_scene_search = draw_panel_scene_search
    blenderkit.download.try_finished_append = try_finished_append
    blenderkit.ui.AssetBarOperator.modal = modal
    blenderkit.upload.get_missing_data_scene = get_missing_data_scene
    bpy.utils.unregister_class(GenerateSceneThumbnailOperator)
    annotations.restore_annotations(
        blenderkit.BlenderKitSceneUploadProps,
        scene_upload_props,
        'bpy.types.Scene.blenderkit'
    )
    annotations.restore_annotations(
        blenderkit.BlenderKitUIProps,
        blenderkit_ui_props,
        'bpy.types.Scene.blenderkitUI'
    )
