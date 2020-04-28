import bpy
import pathlib
import yaml


def yml_to_nodes(yml, directory):
    mat = bpy.data.materials.new(yml['name'])
    mat.use_nodes = True
    tree = mat.node_tree
    tree.nodes.clear()
    for node_description in yml['nodes']:
        print(node_description['name'])
        node = tree.nodes.new(type=node_description['bl_idname'])
        if 'inputs' in node_description:
            for input_description in node_description['inputs']:
                input_ = node.inputs[input_description['name']]
                input_.enabled = input_description['enabled']
                input_.hide = input_description['hide']
                input_.hide_value = input_description['hide_value']
                if 'default_value' in input_description:
                    input_.default_value = eval(str(input_description['default_value']))
        if 'outputs' in node_description:
            for output_description in node_description['outputs']:
                output = node.outputs[output_description['name']]
                output.enabled = output_description['enabled']
                output.hide = output_description['hide']
                output.hide_value = output_description['hide_value']
        for key in node_description:
            if key == 'image':
                node.image = bpy.data.images.load(str(directory.joinpath(node_description[key])))
            elif key not in ['bl_idname', 'inputs', 'outputs']:
                setattr(node, key, node_description[key])

    for link_description in yml['links']:
        output_socket = tree.nodes[link_description['output_node']].outputs[link_description['output_socket']]
        input_socket = tree.nodes[link_description['input_node']].inputs[link_description['input_socket']]
        tree.links.new(output_socket, input_socket)


class ImportNodes(bpy.types.Operator):
    """Import a YAML nodes description to a material"""
    bl_idname = "node.import_nodes"
    bl_label = "Import Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        path = self.filepath
        directory = pathlib.Path(path).parent

        if path.endswith('yml'):
            with open(path) as file:
                yml = yaml.load(file, Loader=yaml.FullLoader)
                yml_to_nodes(yml, directory)
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
