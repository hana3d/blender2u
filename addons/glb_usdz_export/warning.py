from pathlib import Path


def check_file(self, context, file_path, file_name):
    if Path(file_path).stat().st_size > 5 * 2**20:
        print(file_name + " is over 5MB")
        self.report({'WARNING'}, file_name + " is over 5MB")

        def draw(self, context):
            self.layout.label(text=(file_name + " is over 5MB"))

        context.window_manager.popup_menu(draw, title='Exported File Size', icon='ERROR')
    return
