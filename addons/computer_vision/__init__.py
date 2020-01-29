bl_info = {
    "name": "Computer-Vision",
    "author": "Real2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "Unstable addon, use it at your own risks",
    "category": "System"
}


import os
import sys

import bpy
from bpy.app.handlers import persistent

from . import environment, utils, presence
from .libs.replication.replication.constants import RP_COMMON


# TODO: remove dependency as soon as replication will be installed as a module
DEPENDENCIES = {
    ("opencv", "opencv-python")
}


# TODO: refactor config
# UTILITY FUNCTIONS
def generate_supported_types():
    stype_dict = {'supported_types': {}}
    for type in bl_types.types_to_register():
        _type = getattr(bl_types, type)
        props = {}
        props['bl_delay_refresh'] = _type.bl_delay_refresh
        props['bl_delay_apply'] = _type.bl_delay_apply
        props['use_as_filter'] = False
        props['icon'] = _type.bl_icon
        props['auto_push'] = _type.bl_automatic_push
        props['bl_name'] = _type.bl_id

        stype_dict['supported_types'][_type.bl_rep_class.__name__] = props

    return stype_dict


def client_list_callback(scene, context):
    from . import operators
    from .bl_types.bl_user import BlUser

    items = [(RP_COMMON, RP_COMMON, "")]

    username = bpy.context.window_manager.session.username
    cli = operators.client
    if cli:
        client_keys = cli.list(filter=BlUser)
        for k in client_keys:
            name = cli.get(uuid=k).data["name"]

            name_desc = name
            if name == username:
                name_desc += " (self)"

            items.append((name, name_desc, ""))

    return items


class ReplicatedDatablock(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    type_name: bpy.props.StringProperty()
    bl_name: bpy.props.StringProperty()
    bl_delay_refresh: bpy.props.FloatProperty()
    bl_delay_apply: bpy.props.FloatProperty()
    use_as_filter: bpy.props.BoolProperty(default=True)
    auto_push: bpy.props.BoolProperty(default=True)
    icon: bpy.props.StringProperty()


class SessionProps(bpy.types.PropertyGroup):
    username: bpy.props.StringProperty(
        name="Username",
        default="user_{}".format(utils.random_string_digits())
    )
    ip: bpy.props.StringProperty(
        name="ip",
        description='Distant host ip',
        default="127.0.0.1"
    )
    user_uuid: bpy.props.StringProperty(
        name="user_uuid",
        default="None"
    )
    port: bpy.props.IntProperty(
        name="port",
        description='Distant host port',
        default=5555
    )
    add_property_depth: bpy.props.IntProperty(
        name="add_property_depth",
        default=1
    )
    outliner_filter: bpy.props.StringProperty(name="None")
    is_admin: bpy.props.BoolProperty(
        name="is_admin",
        default=False
    )
    init_scene: bpy.props.BoolProperty(
        name="init_scene",
        default=True
    )
    start_empty: bpy.props.BoolProperty(
        name="start_empty",
        default=True
    )
    active_object: bpy.props.PointerProperty(
        name="active_object", type=bpy.types.Object)
    session_mode: bpy.props.EnumProperty(
        name='session_mode',
        description='session mode',
        items={
            ('HOST', 'hosting', 'host a session'),
            ('CONNECT', 'connexion', 'connect to a session')},
        default='HOST')
    right_strategy: bpy.props.EnumProperty(
        name='right_strategy',
        description='right strategy',
        items={
            ('STRICT', 'strict', 'strict right repartition'),
            ('COMMON', 'common', 'relaxed right repartition')},
        default='COMMON')
    client_color: bpy.props.FloatVectorProperty(
        name="client_instance_color",
        subtype='COLOR',
        default = randomColor())
    clients: bpy.props.EnumProperty(
        name="clients",
        description="client enum",
        items=client_list_callback)
    enable_presence: bpy.props.BoolProperty(
        name="Presence overlay",
        description='Enable overlay drawing module',
        default=True,
        update=presence.update_presence
    )
    presence_show_selected: bpy.props.BoolProperty(
        name="Show selected objects",
        description='Enable selection overlay ',
        default=True,
        update=presence.update_overlay_settings
    )
    presence_show_user: bpy.props.BoolProperty(
        name="Show users",
        description='Enable user overlay ',
        default=True,
        update=presence.update_overlay_settings
    )
    supported_datablock: bpy.props.CollectionProperty(
        type=ReplicatedDatablock,
    )
    session_filter: bpy.props.CollectionProperty(
        type=ReplicatedDatablock,
    )
    filter_owned: bpy.props.BoolProperty(
        name="filter_owned",
        description='Show only owned datablocks',
        default=True
    )
    use_select_right: bpy.props.BoolProperty(
        name="Selection right",
        description='Change right on selection',
        default=True
    )

    def load(self):
        config = environment.load_config()
        if "username" in config.keys():
            self.username = config["username"]
            self.ip = config["ip"]
            self.port = config["port"]
            self.start_empty = config["start_empty"]
            self.enable_presence = config["enable_presence"]
            self.client_color = config["client_color"]
        else:
            logger.error("Fail to read user config")

        if len(self.supported_datablock)>0:
            self.supported_datablock.clear()
        if "supported_types" not in config:
            config = generate_supported_types()
        for datablock in config["supported_types"].keys():
            rep_value = self.supported_datablock.add()
            rep_value.name = datablock
            rep_value.type_name = datablock

            config_block = config["supported_types"][datablock]
            rep_value.bl_delay_refresh = config_block['bl_delay_refresh']
            rep_value.bl_delay_apply = config_block['bl_delay_apply']
            rep_value.icon = config_block['icon']
            rep_value.auto_push = config_block['auto_push']
            rep_value.bl_name = config_block['bl_name']

    def save(self,context):
        config = environment.load_config()

        if "supported_types" not in config:
            config = generate_supported_types()

        config["username"] = self.username
        config["ip"] = self.ip
        config["port"] = self.port
        config["start_empty"] = self.start_empty
        config["enable_presence"] = self.enable_presence
        config["client_color"] = [self.client_color.r,self.client_color.g,self.client_color.b]


        for bloc in self.supported_datablock:
            config_block = config["supported_types"][bloc.type_name]
            config_block['bl_delay_refresh'] = bloc.bl_delay_refresh
            config_block['bl_delay_apply'] = bloc.bl_delay_apply
            config_block['use_as_filter'] = bloc.use_as_filter
            config_block['icon'] = bloc.icon
            config_block['auto_push'] = bloc.auto_push
            config_block['bl_name'] = bloc.bl_name
        environment.save_config(config)    


classes = (
    ReplicatedDatablock,
    SessionProps,

)

libs = os.path.dirname(os.path.abspath(__file__)) + "\\libs\\replication"


@persistent
def load_handler(dummy):
    import bpy
    bpy.context.window_manager.session.load()


def register():
    if libs not in sys.path:
        sys.path.append(libs)

    environment.setup(DEPENDENCIES,bpy.app.binary_path_python)

    from . import presence
    from . import operators
    from . import ui

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.session = bpy.props.PointerProperty(
        type=SessionProps)
    bpy.types.ID.uuid = bpy.props.StringProperty(default="")

    bpy.context.window_manager.session.load()

    presence.register()
    operators.register()
    ui.register()
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    from . import presence
    from . import operators
    from . import ui

    presence.unregister()
    ui.unregister()
    operators.unregister()

    del bpy.types.WindowManager.session

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
