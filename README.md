# Voxels-For-Blender
I added support for marching cubes. 

This is made up of 5 scrips Voxels.py, voxelUI.py, marching_cubes_table.py, VoxelsCubes.py, VoxelMarchingCubes.py. I don't know how to get this to work as a plugin. It can be used by making and saving a scene and all the scripts into what ever directory you saved the scene. Then you can open them in the blender text editor which is most easily accessed from the scripting tab way on the top right hand side. push the play button on the voxelUI.py script and a tab named voxel should appear on the UI in the 3d view. You can push 'n' in the 3d view to make the UI visible if its not visible.

The script works by adding extra information to a mesh object so these can be duplicated and edited as any normal mesh object. Be aware that if you do edit the mesh using voxel functions will delete what ever edits you made. Undo functionality works somewhat but not consistently. Voxels works well with modifiers including the subdivision modifier. 

Update Voxel: if you change any of the property settings the voxel will not automatically update. That's what this button is for.

number to use 1: 
number to use 2: these numbers are used by the various voxel editing tools and is used to create different kinds of voxels. for example brick, dirt, rock etc. You need to have a voxel texture and apply it as a material to the object as you would with any other material and object. Voxel number 0 is empty space and can be used to delete voxels

probe voxel number: click on this and then on a voxel to give you its number. For example if you want to use the same brick voxel as you previously used.

Show add Voxels
Add Voxel: adds a new voxel object to the scene with the given dimensions x, y, z. Pick the dimension values carefully as these cant be changed later. The voxel object wont be selected automatically. Select the object to make any voxel changes to it else you'll just get an error when trying to use any voxel editing tools. You can have many voxel objects in the scene.

Show Voxel Options:
Voxel smooth amount: the voxels doesn't have to be cubes they can be smoothed somewhat. 0 to 0.48 is the best smooth range with 0 being blocks. above 0.48 the geometry may start looking weird. Values less than 0 will make the blocks even more jagged than they normally are.
Set voxel smooth: this tool is used to apply the current smoothing value to any voxel you may click on. For example if you want the grass voxels to be smooth click on those and all grass would be smooth.

Fill Voxel (1): fills the entire voxel, good for deleting everything or making caves in a solid block
Replace (1 with 2): replace 1 kind of voxel for another. Good for if you want try different kind of bricks on a wall
rayscan replace(1 with 2): good for surfaces such as grass and snow untop of a rock. use 0 0 1 for direction rayscan to place untop of. setting other values will set other directions for example 0 0 -1 will be below

object to voxel:
will place voxels at any object within the voxel volume. So good for making objects into voxels. Work by tracing upwards and if it find the back of a mesh its considered inside to a plane can be used to place terrain even though it doesn't technically have an inside. It still has back faces. Using 0 for number 1 can be used to quickly delete sections.

tool for editing voxel:
Voxel tool(Q=1, W=2): Use Q to add voxels and W to change existing voxel types. Escape or right click will finish the tool.
Voxel paint tool(Q=1, W=2): Similar to the voxel tool except add or edit large number of voxels in a sphere area at once defined by the brushwidth setting
tool add:
tool edit: these values can be used to finetune where the voxel tool adds and edits. They may need adjusting if you edit smooth voxels or scaled to voxel object. Often easier to set the smoothness to zero make the changes and set the smoothness back.
brushwidth: the radius for the Voxel paint tool to use

Show noise options:
add noise(fill 2 with 1): good for making voxel terrain and caves. select a value for the voxels you want for number 1 and 0 for number 2 to place noise in an empty voxel volume. select 0 for number 1 and what ever your ground is made up of to make caves in a solid volume.
Noise scale: scale of the sampled noise 0.13 seem to generally be a good value
Noise offset: use this if you want different noise or shift the noise in the voxel such that a mountain is in the center instead of the side.
Noise: type of noise to use. Blender offers quite a few flavors of noise.

uv settings:
This voxel tool will automatically generate uv's for the voxels. The uv's start in the bottom left corner then move to right and up for each additional block. each block is made up of top center and bottom uv's so that things like grass covering the top can be mapped. Ideal uv map is 3 times as tall as its wide else the blocks may seem squashed.
uv scale: the amount of uvs to the side of a square. scale of 10 for example will mean theres 100 (10 x 10) uv maps in total each made up of 3 squares one for top center and bottom.
uv buffer: the gap between squares on the uv map. Stops bleeding which causes ugly lines. low value such as 0.02 should be sufficient.
top cover: used by marching cubes and affects the amount of top texture mapped to the voxels. Marching cubes use the same texture map as normal voxels.
bottom cover: used by marching cubes and affects the amount of bottom texture mapped to the voxels. Marching cubes use the same texture map as normal voxels.
