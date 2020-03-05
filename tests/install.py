import addon_utils


class NewError(Exception):
    """Base class for other exceptions"""
    pass


if addon_utils.enable("blender2u", default_set=False, persistent=True, handle_error=None) is None:
    raise NewError
