import addon_utils


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InstallError(Error):
    """Raised when the install fails"""
    pass


if addon_utils.enable("blender2u", default_set=False, persistent=True, handle_error=None) is None:
    raise InstallError
