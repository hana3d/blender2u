import bpy
import os
import pathlib
from zipfile import ZipFile


class SingleMaterial(bpy.types.Operator):
    """Import a single material from a input file, can be either jpg/png or zip"""
    bl_idname = "material.single_import"
    bl_label = "Import Material"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty()

    def create_base_material(self, tree, main_node, name, path):
        base_color_node = tree.nodes.new(type='ShaderNodeTexImage')
        base_color_node.location = -500, 500
        base_color_node.image = bpy.data.images.load(path)

        tree.links.new(base_color_node.outputs['Color'], main_node.inputs['Base Color'])

        if 'metal' in name:
            main_node.inputs['Metallic'].default_value = 1.0

    def create_maps_material(self, tree, main_node, name, path):
        extract_path = pathlib.Path(path).parent.joinpath(name)
        if not os.path.exists(extract_path):
            os.mkdir(extract_path)
            with ZipFile(path, 'r') as zip_file:
                zip_file.extractall(path=extract_path)
        for image in extract_path.iterdir():
            image = str(image)
            if any(s in image for s in ['_col.', '_COL.', '_diff_2k.']):
                base_color_node = tree.nodes.new(type='ShaderNodeTexImage')
                base_color_node.location = -500, 500
                base_color_node.image = bpy.data.images.load(image)
                tree.links.new(base_color_node.outputs['Color'], main_node.inputs['Base Color'])
            elif any(s in image for s in ['_met.', '_MET.']):
                metal_node = tree.nodes.new(type='ShaderNodeTexImage')
                metal_node.location = -500, 250
                metal_node.image = bpy.data.images.load(image)
                tree.links.new(metal_node.outputs['Color'], main_node.inputs['Metallic'])
            elif any(s in image for s in ['_spec_2k.']):
                if 'metal' in image:
                    main_node.inputs['Metallic'].default_value = 1.0
                specular_node = tree.nodes.new(type='ShaderNodeTexImage')
                specular_node.location = -500, 250
                specular_node.image = bpy.data.images.load(image)
                tree.links.new(specular_node.outputs['Color'], main_node.inputs['Specular'])
            elif any(s in image for s in ['_rgh.', '_RGH.', '_rough_2k.']):
                roughness_node = tree.nodes.new(type='ShaderNodeTexImage')
                roughness_node.location = -500, 0
                roughness_node.image = bpy.data.images.load(image)
                tree.links.new(roughness_node.outputs['Color'], main_node.inputs['Roughness'])
            elif any(s in image for s in ['_nrm.', '_NRM.', '_Nor_2k.', '_nor_2k.']):
                normal_tex_node = tree.nodes.new(type='ShaderNodeTexImage')
                normal_tex_node.location = -500, -250
                normal_tex_node.image = bpy.data.images.load(image)
                normal_node = tree.nodes.new(type='ShaderNodeNormalMap')
                normal_node.location = -200, -250
                tree.links.new(normal_tex_node.outputs['Color'], normal_node.inputs['Color'])
                tree.links.new(normal_node.outputs['Normal'], main_node.inputs['Normal'])

    def execute(self, context):
        path = self.filepath
        name = pathlib.Path(path).stem

        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        tree = mat.node_tree
        main_node = tree.nodes['Principled BSDF']

        if path.endswith('png') or path.endswith('jpg'):
            self.create_base_material(tree, main_node, name, path)
        elif path.endswith('zip'):
            self.create_maps_material(tree, main_node, name, path)
        else:
            self.report({'ERROR'}, "invalid file")

        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except:
            print('Addon analytics not installed')

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}
