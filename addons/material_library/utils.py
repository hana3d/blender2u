import bpy


def get_material(name):
    # matlib = bpy.context.scene.matlib
    # material = None

    # for mat in bpy.data.materials:
    #     try:
    #         samelib = bpy.path.relpath(mat.library.filepath) == bpy.path.relpath(
    #             matlib.current_library.path)
    #     except:
    #         samelib = False

    #     if mat.name == name and mat.library and samelib:
    #         material = mat
    #         break

    # if not force:
    #     # busca materiales no linkados
    #     for mat in bpy.data.materials:
    #         if mat.name == name and not mat.library:
    #             material = mat
    #             break

    # if not material:
    #     import_material(name)

    if not bpy.data.materials.get(name):
        import_material(name)


def import_material(name, link=False):
    matlib = bpy.context.scene.matlib
    with bpy.data.libraries.load(matlib.current_library.path, link, False) as (data_from, data_to):
        data_to.materials = [name]
