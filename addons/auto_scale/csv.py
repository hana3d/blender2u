import csv
import io
import bpy
from mathutils import Vector


class ObjectCSVScale(bpy.types.Operator):
    """Object CSV Scale"""
    bl_idname = "object.csv_scale"
    bl_label = "Automatic Scale with CSV"
    bl_options = {'REGISTER', 'UNDO'}

    # Define this to tell 'fileselect_add' that we want a directoy
    filepath: bpy.props.StringProperty(
        name="CSV File",
        description="CSV with heights and names",
        subtype='FILE_PATH'
    )

    def scale_coll(self, context, reader, coll):
        min_x = 999999
        min_y = 999999
        min_z = 999999
        max_x = -999999
        max_y = -999999
        max_z = -999999
        for row in reader:
            if row['sku'] in coll.name:
                message = '[' + row['sku'] + ']'
                valid_object = False
                for obj in coll.objects:
                    if (obj.visible_get()) and obj.type != 'EMPTY':
                        valid_object = True
                        obj.select_set(True)
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)

                        for vertex in [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]:
                            min_x = (min_x, vertex[0])[vertex[0] < min_x]
                            min_y = (min_y, vertex[1])[vertex[1] < min_y]
                            min_z = (min_z, vertex[2])[vertex[2] < min_z]
                            max_x = (max_x, vertex[0])[vertex[0] > max_x]
                            max_y = (max_y, vertex[1])[vertex[1] > max_y]
                            max_z = (max_z, vertex[2])[vertex[2] > max_z]

                if not valid_object:
                    message += ' - not valid'
                    print(message)
                    return
                if row['height']:
                    size_z = max_z - min_z
                    scale = float(row['height']) / size_z
                    message += ' - size ' + str(size_z)
                    message += ' - height ' + row['height']
                elif row['length']:
                    size_x = max_x - min_x
                    size_y = max_y - min_y
                    scale = (float(row['length']) / size_x) if (size_x > size_y) else (float(row['length']) / size_y)
                    message += ' - length ' + row['length']
                else:
                    context.view_layer.layer_collection.children[coll.name].hide_viewport = True
                    message += ' - not scaled' + row['height'] + row['length']
                    print(message)
                    return
                bpy.ops.transform.resize(value=(scale, scale, scale))
                message += ' - scale: ' + str(scale)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)
                print(message)
                return

    def execute(self, context):
        bpy.ops.analytics.addons_analytics(self.bl_label)

        csv_filepath = self.filepath

        with io.open(csv_filepath, newline='') as csvfile:
            reader = list(csv.DictReader(csvfile))

            collections = bpy.data.collections

            for coll in collections:

                bpy.ops.object.select_all(action='DESELECT')
                self.scale_coll(reader, coll)

        return {'FINISHED'}

    def invoke(self, context, event):
        # Open browser, take reference to 'self' read the path to selected
        # file, put path in predetermined self fields.
        # See: https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        context.window_manager.fileselect_add(self)
        # Tells Blender to hang on for the slow user input
        return {'RUNNING_MODAL'}
