import bpy
import blenderkit


draw_panel_model_upload = blenderkit.ui_panels.draw_panel_model_upload
draw_panel_material_upload = blenderkit.ui_panels.draw_panel_material_upload
upload_invoke = blenderkit.upload.UploadOperator.invoke


def upload_invoke2(self, context, event):
    return self.execute(context)


def label_multiline(layout, text='', icon='NONE', width=-1):
    ''' draw a ui label, but try to split it in multiple lines.'''
    if text.strip() == '':
        return
    lines = text.split('\n')
    if width > 0:
        threshold = int(width / 5.5)
    else:
        threshold = 35
    maxlines = 8
    li = 0
    for line in lines:
        while len(line) > threshold:
            i = line.rfind(' ', 0, threshold)
            if i < 1:
                i = threshold
            l1 = line[:i]
            layout.label(text=l1, icon=icon)
            icon = 'NONE'
            line = line[i:].lstrip()
            li += 1
            if li > maxlines:
                break
        if li > maxlines:
            break
        layout.label(text=line, icon=icon)
        icon = 'NONE'


def prop_needed(layout, props, name, value, is_not_filled=''):
    row = layout.row()
    if value == is_not_filled:
        row.alert = True
        row.prop(props, name)
        row.alert = False
    else:
        row.prop(props, name)


def draw_upload_common(layout, props, asset_type, context):
    layout.row(align=True)
    if props.upload_state != '':
        label_multiline(layout, text=props.upload_state, width=context.region.width)
    if props.uploading:
        op = layout.operator('object.kill_bg_process', text="", icon='CANCEL')
        op.process_source = asset_type
        op.process_type = 'UPLOAD'
        layout = layout.column()
        layout.enabled = False

    if props.asset_base_id == '':
        optext = 'Upload %s' % asset_type.lower()
        op = layout.operator("object.blenderkit_upload", text=optext, icon='EXPORT')
        op.asset_type = asset_type

    if props.asset_base_id != '':
        op = layout.operator("object.blenderkit_upload", text='Reupload asset', icon='EXPORT')
        op.asset_type = asset_type
        op.reupload = True

        op = layout.operator("object.blenderkit_upload", text='Upload as new asset', icon='EXPORT')
        op.asset_type = asset_type
        op.reupload = False

        layout.label(text='asset has a version online.')


def draw_panel_model_upload2(self, context):
    scene = context.scene
    ob = bpy.context.active_object
    while ob.parent is not None:
        ob = ob.parent
    props = ob.blenderkit

    layout = self.layout

    draw_upload_common(layout, props, 'MODEL', context)

    prop_needed(layout, props, 'name', props.name)

    col = layout.column()
    if props.is_generating_thumbnail:
        col.enabled = False
    prop_needed(col, props, 'thumbnail', props.has_thumbnail, False)
    if bpy.context.scene.render.engine in ('CYCLES', 'BLENDER_EEVEE'):
        col.operator("object.blenderkit_generate_thumbnail", text='Generate thumbnail', icon='IMAGE')

    if props.is_generating_thumbnail:
        row = layout.row(align=True)
        row.label(text=props.thumbnail_generating_state)
        op = row.operator('object.kill_bg_process', text="", icon='CANCEL')
        op.process_source = 'MODEL'
        op.process_type = 'THUMBNAILER'
    elif props.thumbnail_generating_state != '':
        label_multiline(layout, text=props.thumbnail_generating_state)

    layout.prop(props, 'description')
    layout.prop(props, 'tags')
    layout.prop(props, 'client')
    layout.prop(props, 'sku')

    for key in props.custom_props.keys():
        layout.prop(props.custom_props, f'["{key}"]')

    row = layout.row()
    row.operator('blenderkit.model_custom_props', text='Create Custom Prop')
    layout.prop(scene.blenderkit_custom_props, "key")
    layout.prop(scene.blenderkit_custom_props, "value")


def draw_panel_material_upload2(self, context):
    scene = context.scene
    mat = bpy.context.active_object.active_material

    props = mat.blenderkit
    layout = self.layout

    draw_upload_common(layout, props, 'MATERIAL', context)

    prop_needed(layout, props, 'name', props.name)
    layout.prop(props, 'description')
    layout.prop(props, 'tags')
    layout.prop(props, 'client')
    layout.prop(props, 'sku')

    for key in props.custom_props.keys():
        layout.prop(props.custom_props, f'["{key}"]')

    row = layout.row()
    row.operator('blenderkit.material_custom_props', text='Create Custom Prop')
    layout.prop(scene.blenderkit_custom_props, "key")
    layout.prop(scene.blenderkit_custom_props, "value")

    row = layout.row()
    if props.is_generating_thumbnail:
        row.enabled = False
    prop_needed(row, props, 'thumbnail', props.has_thumbnail, False)

    if props.is_generating_thumbnail:
        row = layout.row(align=True)
        row.label(text=props.thumbnail_generating_state, icon='RENDER_STILL')
        op = row.operator('object.kill_bg_process', text="", icon='CANCEL')
        op.process_source = 'MATERIAL'
        op.process_type = 'THUMBNAILER'
    elif props.thumbnail_generating_state != '':
        label_multiline(layout, text=props.thumbnail_generating_state)

    if bpy.context.scene.render.engine in ('CYCLES', 'BLENDER_EEVEE'):
        layout.operator("object.blenderkit_material_thumbnail", text='Render thumbnail with Cycles', icon='EXPORT')


class VIEW3D_PT_blenderkit_header(bpy.types.Panel):
    bl_category = "BlenderKit"
    bl_idname = "VIEW3D_PT_blenderkit_downloads"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Header"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.preferences.addons['blenderkit'].preferences, 'search_in_header')


def register():
    bpy.utils.register_class(VIEW3D_PT_blenderkit_header)
    blenderkit.upload.UploadOperator.invoke = upload_invoke2
    blenderkit.ui_panels.draw_panel_model_upload = draw_panel_model_upload2
    blenderkit.ui_panels.draw_panel_material_upload = draw_panel_material_upload2


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_blenderkit_header)
    blenderkit.upload.UploadOperator.invoke = upload_invoke
    blenderkit.ui_panels.draw_panel_model_upload = draw_panel_model_upload
    blenderkit.ui_panels.draw_panel_material_upload = draw_panel_material_upload
