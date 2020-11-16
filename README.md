# Blender2U

To develop on this project, setup `fake-bpy`, to help with linting and code completion

```
python -m virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
```

Collection of Blender Add-ons made by R2U.

1. [Analytics](#analytics)
2. [Auto Scale](#auto-scale)
3. [Bake Nodes](#bake-nodes)
4. [Collections Grid](#collections-grid)
5. [GLB Export](#glb-export)
6. [Material Library](#material-library)
7. [Mesh Lint](#mesh-lint)
8. [Nodes IO](#nodes-io)
9. [Polycount](#polycount)
10. [BlenderCV / Mesh Countour](#mesh-contour)
11. [BlenderCV / Edges Mesh](#edges-mesh)

## Analytics
Sends some user data to AWS S3 for future analysis.

## Auto Scale
Scale all selected objects so that the combination of them has a total height or length equal to the value inputed by the user.

By default, it uses *height* for scaling the object, unless `Use length` is checked.

It is also possible to scale objects in the scene according to the information from an inputed CSV file.  

## Bake Nodes

Automatically bakes the nodes of the active material into a image, for every object of the active collection.

## Collections Grid

Organizes all scene collections in a grid according to the inputed number of rows and distance between the collections.

If the `Object Grid` option is checked, it organizes a grid with all the objects in the scene instead of collections.

## GLB Export

Easily export all collections from the scene to glb format.

## Material Library

Creates a library system for materials to be easily catalogued, shared and visualized.  

## Mesh Lint

Checks if a mesh meets certain criteria of good practices, like no use of tris, ngons or nonmanifold elements.

Location: `Object Data properties > MeshLint`

## Nodes IO

Export and import nodes described as yaml.

## Polycount

Prints to the console, in descending order, the percentage of the total polygons that each object in the scene represents.

Adds a Heatmap tool that shows in brighter red which objects in the active collection have more polygons.  
(Takes into account the Decimate Modifier).

## UV Check

Apply a checker texture to all scene objects for easier UV check.  

## BlenderCV

Implementation of some OpenCV methods to help modelling in Blender using reference images.

#### Mesh Contour

Find Contours with gray value threshold to separate the object in a image from a white background and creates a mesh plane with that shape.

Some parameters can be adjusted to determine the number of vertices.

#### Edges Mesh

Uses Edges Canny to draw the vertices of the detected edges of a selected region of a image.