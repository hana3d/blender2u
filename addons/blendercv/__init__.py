bl_info = {
    "name": "BlenderCV",
    "author": "Real2U",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "category": "System"
}


# import os
# import sys
import bpy
from . import environment
# from .libs.replication.replication.constants import RP_COMMON


DEPENDENCIES = {
    ("cv2", "opencv-python")
}

# libs = os.path.dirname(os.path.abspath(__file__)) + "\\libs\\replication"


def register():
    # if libs not in sys.path:
    #     sys.path.append(libs)

    environment.setup(DEPENDENCIES, bpy.app.binary_path_python)

    from . import main
    main.register()


def unregister():
    from . import main
    main.unregister()
