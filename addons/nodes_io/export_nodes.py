import bpy
import os
import yaml


def nodes_to_yml(material, directory):
    header = {
        'blender_version': str(bpy.app.version),
        'nodes_io_version': 0.01,
        'name': material.name,
        'nodes_number': len(material.node_tree.nodes)
    }
    nodes = []
    for node in material.node_tree.nodes:
        node_data = {
            'bl_idname': node.bl_idname,
        }
        if len(node.inputs) > 0:
            inputs = []
            for input_ in node.inputs:
                input_data = {
                    'name': input_.name,
                    'enabled': input_.enabled,
                    'hide': input_.hide,
                    'hide_value': input_.hide_value,
                    'is_linked': input_.is_linked
                }
                if hasattr(input_, 'default_value'):
                    if isinstance(input_.default_value, float):
                        input_data['default_value'] = round(input_.default_value, 3)
                    else:
                        data = []
                        for elem in list(input_.default_value):
                            if isinstance(elem, float):
                                data.append(round(elem, 3))
                            else:
                                data.append(elem)
                        input_data['default_value'] = data
                inputs.append(input_data)
            node_data['inputs'] = inputs
        if len(node.outputs) > 0:
            outputs = []
            for output in node.outputs:
                outputs.append({
                    'name': output.name,
                    'enabled': output.enabled,
                    'hide': output.hide,
                    'hide_value': output.hide_value,
                    'is_linked': output.is_linked
                })
            node_data['outputs'] = outputs
        for prop in dir(node):
            try:
                if node.is_property_readonly(prop):
                    continue
                if isinstance(getattr(node, prop), (int, str, bool)):
                    node_data[prop] = getattr(node, prop)
                elif isinstance(getattr(node, prop), float):
                    node_data[prop] = round(getattr(node, prop), 3)
                elif isinstance(getattr(node, prop), bpy.types.Image):
                    img_path = directory + os.sep + getattr(node, prop).name
                    getattr(node, prop).save_render(img_path)
                    node_data[prop] = getattr(node, prop).name
                else:
                    data = []
                    for elem in list(getattr(node, prop)):
                        if isinstance(elem, float):
                            data.append(round(elem, 3))
                        else:
                            data.append(elem)
                    node_data[prop] = data
            except:
                pass
        nodes.append(node_data)
    links = []
    for link in material.node_tree.links:
        links.append({
            'output_node': link.from_node.name,
            'output_socket': link.from_socket.name,
            'input_node': link.to_node.name,
            'input_socket': link.to_socket.name
        })
    header['nodes'] = nodes
    header['links'] = links
    return header


class ExportNodes(bpy.types.Operator):
    """Exports nodes description from input material to YAML format"""
    bl_idname = "node.export_nodes"
    bl_label = "Export Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty()
    material: bpy.types.Material

    def execute(self, context):
        path = self.directory + os.sep + self.material.name + '.yml'

        yml = nodes_to_yml(self.material, self.directory)
        with open(path, 'w') as file:
            yaml.dump(yml, file)

        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            bpy.ops.analytics.addons_analytics('EXEC_DEFAULT', operator_name=self.bl_label)
        except:
            print('Addon analytics not installed')

        self.material = context.active_object.active_material

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}
