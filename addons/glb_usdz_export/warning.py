import ctypes
from pathlib import Path


def check_file(self, context, file_path, file_name):
    if Path(file_path).stat().st_size > 5 * 2**20:
        print(file_name + " is over 5MB")
        self.report({'WARNING'}, file_name + " is over 5MB")

        ctypes.windll.user32.MessageBoxW(0, file_name + " is over 5MB", "Exported File Size", 0)
    return
