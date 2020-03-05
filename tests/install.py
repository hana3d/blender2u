import addon_utils


class NewError(Exception):
    """Base class for other exceptions"""
    pass


def handle_error():
    NewError


addon_utils.enable("blender2u", default_set=False, persistent=True, handle_error=handle_error())
