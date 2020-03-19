import bpy


class CreateWorkspace(bpy.types.Operator):
    """Create Workspace"""
    bl_idname = "matlib.create_workspace"
    bl_label = "Create Workspace"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.window.workspace = bpy.data.workspaces['Layout']
        bpy.ops.workspace.duplicate()
        bpy.data.workspaces['Layout.001'].name = 'Matlib'

        bpy.ops.scene.new(type='NEW')
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, location=(0, 0, 0))

        for obj in context.scene.objects:
            obj.active_material = bpy.data.materials['Material']

        return {'FINISHED'}
