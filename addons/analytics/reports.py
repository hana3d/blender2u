import bpy


# save the current area
area = bpy.context.area.type

# set the context
bpy.context.area.type = 'INFO'

bpy.ops.info.select_all(action='SELECT')
bpy.ops.info.report_copy()

# leave the context where it was
bpy.context.area.type = area
