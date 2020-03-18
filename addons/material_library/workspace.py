import bpy


class CreateWorkspace(bpy.types.Operator):
    """Create Workspace"""
    bl_idname = "matlib.create_workspace"
    bl_label = "Create Workspace"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces['Layout']
        bpy.ops.workspace.duplicate()
        bpy.data.workspaces['Layout.001'].name = 'Matlib'
        bpy.ops.workspace.reorder_to_back()

        return {'FINISHED'}
