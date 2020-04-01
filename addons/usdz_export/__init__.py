# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "usdz-export",
    "author": "real2u",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": "Import-Export"
}

import os
import shutil
import stat
import bpy
import platform
from distutils.dir_util import copy_tree
from .panel import OBJECT_PT_USDZExporterPanel


class USDZExporter(bpy.types.Operator):
    """USDZ Exporter"""
    bl_idname = "export_scene.usdz_export"
    bl_label = "USDZ Export"
    bl_options = {'REGISTER', 'UNDO'}

    # Define this to tell 'fileselect_add' that we want a directoy
    directory: bpy.props.StringProperty(
        name="Outdir Path",
        description="Where I will save my stuff"
        # subtype='DIR_PATH' is not needed to specify the selection mode.
        # But this will be anyway a directory path.
    )

    def execute(self, context):
        bpy.ops.analytics.addons_analytics(self.bl_label)

        if os.path.exists(bpy.utils.resource_path('USER').replace(' ', '') + os.sep + 'scripts' + os.sep + 'addons'
                          + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'usdz_export' + os.sep + 'usdz-exporter'):
            docker_path = bpy.utils.resource_path('USER').replace(' ', '') + os.sep + 'scripts' + os.sep + 'addons' \
                + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'usdz_export' + os.sep + 'usdz-exporter'
        elif os.path.exists(bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons'
                            + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'usdz_export' + os.sep + 'usdz-exporter'):
            docker_path = bpy.utils.resource_path('USER') + os.sep + 'scripts' + os.sep + 'addons' \
                + os.sep + 'blender2u' + os.sep + 'addons' + os.sep + 'usdz_export' + os.sep + 'usdz-exporter'
        else:
            self.report({'ERROR'}, "usdz-exporter path not found")
            return {'CANCELLED'}

        root = self.directory

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

        copy_tree(bpy.path.abspath(root), docker_path + os.sep + 'prod' + os.sep + 'input')
        loginCmd = 'aws ecr get-login-password \
                        --region us-east-1 \
                    | docker login \
                        --username AWS \
                        --password-stdin 715293289758.dkr.ecr.us-east-1.amazonaws.com'
        if platform.system() == 'Darwin':
            runCmd = 'docker run --rm --name usdz-extractor-container-prod -v $(PWD)/prod/output:/usdz-exporter/output -it usdz-extractor-image-prod'
        elif platform.system() == 'Linux':
            runCmd = 'docker run --rm --name usdz-extractor-container-prod -v $(PWD)/prod/output:/usdz-exporter/output -it usdz-extractor-image-prod'
        elif platform.system() == 'Windows':
            runCmd = 'docker run --rm --name usdz-extractor-container-prod -v "' + docker_path.replace("\\", "/").lower() \
                + '/prod/output":/usdz-exporter/output -it usdz-extractor-image-prod'
        os.system(loginCmd)
        cdCmd = 'cd ' + docker_path
        buildCmd = 'docker build ./prod -t usdz-extractor-image-prod'
        command = cdCmd + ' && ' + buildCmd + ' && ' + runCmd
        os.system(command)
        if not os.path.exists(bpy.path.abspath(root + 'usdz/')):
            os.mkdir(bpy.path.abspath(root + 'usdz/'))
        copy_tree(docker_path + os.sep + 'prod' + os.sep + 'output' + os.sep + '.', bpy.path.abspath(root + 'usdz/'))
        shutil.rmtree(docker_path + os.sep + 'prod' + os.sep + 'input/')
        shutil.rmtree(docker_path + os.sep + 'prod' + os.sep + 'output/')
        return {'FINISHED'}

    def invoke(self, context, event):
        # Open browser, take reference to 'self' read the path to selected
        # file, put path in predetermined self fields.
        # See: https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        context.window_manager.fileselect_add(self)
        # Tells Blender to hang on for the slow user input
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    self.layout.operator(USDZExporter.bl_idname)


def register():
    bpy.utils.register_class(USDZExporter)
    bpy.utils.register_class(OBJECT_PT_USDZExporterPanel)
    # bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_class(USDZExporter)
    bpy.utils.unregister_class(OBJECT_PT_USDZExporterPanel)
    # bpy.types.TOPBAR_MT_file_export.remove(menu_func)


if __name__ == "__main__":
    register()
