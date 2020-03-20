import bpy


def create_workspace(context: bpy.types.Context, workspace_type: str, name: str):
    """Creates a new workspace tab"""
    context.window.workspace = bpy.data.workspaces[workspace_type]
    bpy.ops.workspace.duplicate()
    bpy.data.workspaces[workspace_type + '.001'].name = name
