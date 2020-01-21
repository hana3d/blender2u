# Blender2U

Collection of Blender Add-ons made by Real2U.

## Analytics
Sends some user data to AWS S3 for future analysis.

## Auto Scale  
Scale all selected objects so that the combination of them has a total height or 
length equal to the value inputed by the user.  
If box "Use length" is checked it uses only the length for scaling, 
otherwise it uses only the height.  
Also can scale objects in the scene according to the information from an inputed csv file.  

## Bake Nodes  
Automatically bakes the nodes of the active material into a image, for every object of the active collection.

## Collection Grid  
Organizes all scene collections in a grid according to the inputed number of rows and distance between collections.  
Object Grid option organizes a grid with all the objects in the scene instead of collections.  

## GLB Export  
Easily export all collections from the scene to glb format.  

## GLB USDZ Export  
### Requirements
[**Install Docker**](https://docs.docker.com/docker-for-windows/install/)  
[**Install AWS CLI**](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/install-windows.html)
and [**configure it**](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/cli-chap-configure.html)    

Does GLB Export and USDZ Export in sequence to automatically export both glb and usdz files ready to be used.  
**On Mac and Linux, Blender has to be initialized by a terminal.**(How to:
[Linux](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/linux.html),
[Mac](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/macos.html))  

## Polycount  
Prints in the console, in order, the percentage of the total polygons that each object in the scene represents.  
Adds a Heatmap tool that shows in brighter red which objects in the active collection have more polygons.  
(Takes into account the Decimate Modifier).  

## USDZ Export  
Uses [Docker USDZ Exporter](https://gitlab.com/real2u/usdz-exporter)  
### Requirements
[**Install Docker**](https://docs.docker.com/docker-for-windows/install/)  
[**Install AWS CLI**](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/install-windows.html)
and [**configure it**](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/cli-chap-configure.html)    

Converts the files from the selected folder to usdz using a environment dependent python script inside a container.  
**On Mac and Linux, Blender has to be initialized by a terminal.**(How to:
[Linux](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/linux.html),
[Mac](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/macos.html))  