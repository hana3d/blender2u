import os
import shutil
import stat
import platform
import bpy
from distutils.dir_util import copy_tree
from mathutils import Vector


class GLBUSDZExport(bpy.types.Operator):
    """GLB USDZ Export"""
    bl_idname = "object.glb_usdz_export"
    bl_label = "GLB and USDZ Export"
    bl_options = {'REGISTER', 'UNDO'}

    # Define this to tell 'fileselect_add' that we want a directoy
    directory = bpy.props.StringProperty(
        name="Outdir Path",
        description="Where I will save my stuff"
        # subtype='DIR_PATH' is not needed to specify the selection mode.
        # But this will be anyway a directory path.
    )

    def execute(self, context):
        context.view_layer.active_layer_collection = context.scene.view_layers[0].layer_collection

        if os.path.exists(bpy.utils.resource_path('USER').replace(' ', '') + os.sep + 'scripts' + os.sep + 'addons' + os.sep + 'blender2u' + os.sep + 'usdz-exporter'):
            docker_path = bpy.utils.resource_path('USER').replace(' ', '') + os.sep + 'scripts' + os.sep + 'addons' + os.sep + 'blender2u' + os.sep + 'usdz-exporter'
        elif os.path.exists(bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' + os.sep + 'blender2u' + os.sep + 'usdz-exporter'):
            docker_path = bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' + os.sep + 'blender2u' + os.sep + 'usdz-exporter'
        else:
            self.report({'ERROR'}, "usdz-exporter path not found")
            return {'CANCELLED'}

        root = self.directory

        if not os.path.exists(bpy.path.abspath(root + 'tmp/')):
            os.mkdir(bpy.path.abspath(root + 'tmp/'))
        else:
            shutil.rmtree(bpy.path.abspath(root + 'tmp/'))
            os.mkdir(bpy.path.abspath(root + 'tmp/'))
        path = bpy.path.abspath(root + 'tmp/')

        if not os.path.exists(bpy.path.abspath(root + 'glb/')):
            os.mkdir(bpy.path.abspath(root + 'glb/'))

        try:
            bpy.ops.object.select_all(action='SELECT')
            print('select')
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            print('clear parent')
            bpy.ops.object.select_by_type(extend=False, type='EMPTY')
            print('select empty')
            bpy.ops.object.delete(use_global=True, confirm=False)
        except:
            print('No empties')

        collections = bpy.data.collections

        bpy.ops.object.select_all(action='DESELECT')
        for coll in collections:
            if coll.hide_viewport is True or context.view_layer.layer_collection.children[coll.name].hide_viewport is True:
                continue

            min_x = 999999
            min_y = 999999
            max_x = -999999
            max_y = -999999

            valid_object = False

            for obj in coll.objects:
                if (obj.visible_get()):
                    valid_object = True
                    obj.select_set(True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=False)

                    # bake_nodes(obj)

                    for vertex in [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]:
                        min_x = (min_x, vertex[0])[vertex[0] < min_x]
                        min_y = (min_y, vertex[1])[vertex[1] < min_y]
                        # min_z = (min_z, vertex[2])[vertex[2] < min_z]
                        max_x = (max_x, vertex[0])[vertex[0] > max_x]
                        max_y = (max_y, vertex[1])[vertex[1] > max_y]
                        # max_z = (max_z, vertex[2])[vertex[2] > max_z]

                    bpy.ops.object.select_all(action='DESELECT')

            if not valid_object:
                continue

            center_x = min_x + (max_x - min_x) / 2
            center_y = min_y + (max_y - min_y) / 2
            bpy.ops.object.add(type='EMPTY', location=(center_x, center_y, 0.0))
            empty = bpy.context.selected_objects[0]
            coll.objects.link(empty)
            bpy.context.view_layer.active_layer_collection.collection.objects.unlink(empty)

            bpy.context.view_layer.objects.active = empty

            bpy.ops.object.select_all(action='DESELECT')
            for obj in coll.objects:
                if obj != empty:
                    if (obj.visible_get()):
                        obj.select_set(True)

            bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
            bpy.ops.object.select_all(action='DESELECT')
            empty.select_set(True)

            location = empty.location.copy()
            empty.location.x = 0
            empty.location.y = 0
            for select in coll.objects:
                if (select.visible_get()):
                    select.select_set(True)
            filename = path + coll.name + '.glb'
            bpy.ops.export_scene.gltf(filepath=filename, export_selected=True, export_apply=True)
            empty.location = location

            bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.select_by_type(extend=False, type='EMPTY')
        bpy.ops.object.delete(use_global=True, confirm=False)

        os.chmod(docker_path + os.sep + 'prod' + os.sep + 'convert.sh', stat.S_IRWXU or stat.S_IXGRP or stat.S_IXOTH)
        if not os.path.exists(bpy.path.abspath(docker_path + os.sep + 'prod' + os.sep + 'input/')):
            os.mkdir(bpy.path.abspath(bpy.path.abspath(docker_path + os.sep + 'prod' + os.sep + 'input/')))
        else:
            shutil.rmtree(docker_path + os.sep + 'prod' + os.sep + 'input/')
            os.mkdir(bpy.path.abspath(bpy.path.abspath(docker_path + os.sep + 'prod' + os.sep + 'input/')))

        if not os.path.exists(bpy.path.abspath(docker_path + os.sep + 'prod' + os.sep + 'output/')):
            os.mkdir(bpy.path.abspath(bpy.path.abspath(docker_path + os.sep + 'prod' + os.sep + 'output/')))
        else:
            shutil.rmtree(docker_path + os.sep + 'prod' + os.sep + 'output/')
            os.mkdir(bpy.path.abspath(bpy.path.abspath(docker_path + os.sep + 'prod' + os.sep + 'output/')))

        if not os.path.exists(bpy.path.abspath(root + 'usdz/')):
            os.mkdir(bpy.path.abspath(root + 'usdz/'))
        copy_tree(bpy.path.abspath(root + 'tmp/'), docker_path + os.sep + 'prod' + os.sep + 'input')
        copy_tree(bpy.path.abspath(root + 'tmp/'), bpy.path.abspath(root + 'glb/'))
        if platform.system() == 'Darwin':
            loginCmd = '$(aws ecr get-login --no-include-email --region us-east-1)'
            runCmd = 'docker run --rm --name usdz-extractor-container-prod -v $(PWD)/prod/output:/usdz-exporter/output -it usdz-extractor-image-prod'
        elif platform.system() == 'Linux':
            loginCmd = '$(aws ecr get-login --no-include-email --region us-east-1)'
            runCmd = 'docker run --rm --name usdz-extractor-container-prod -v $(PWD)/prod/output:/usdz-exporter/output -it usdz-extractor-image-prod'
        elif platform.system() == 'Windows':
            loginCmd = 'FOR /F "tokens=* USEBACKQ" %F IN (`aws ecr get-login --no-include-email --region us-east-1`) DO (SET var=%F) && call %var%'
            runCmd = 'docker run --rm --name usdz-extractor-container-prod -v "' + docker_path.replace("\\", "/").lower() + '/prod/output":/usdz-exporter/output -it usdz-extractor-image-prod'
        os.system(loginCmd)
        cdCmd = 'cd ' + docker_path
        buildCmd = 'docker build ./prod -t usdz-extractor-image-prod'
        command = cdCmd + ' && ' + buildCmd + ' && ' + runCmd
        os.system(command)
        copy_tree(docker_path + os.sep + 'prod' + os.sep + 'output' + os.sep + '.', bpy.path.abspath(root + 'usdz/'))
        shutil.rmtree(docker_path + os.sep + 'prod' + os.sep + 'input/')
        shutil.rmtree(docker_path + os.sep + 'prod' + os.sep + 'output/')
        shutil.rmtree(bpy.path.abspath(root + 'tmp/'))
        return {'FINISHED'}

    def invoke(self, context, event):
        # Open browser, take reference to 'self' read the path to selected
        # file, put path in predetermined self fields.
        # See: https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        context.window_manager.fileselect_add(self)
        # Tells Blender to hang on for the slow user input
        return {'RUNNING_MODAL'}
