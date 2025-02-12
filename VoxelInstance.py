import bpy
import bmesh
import numpy as np
import mathutils
import math
import re

def num_sort(obj):
    return list(map(int, re.findall(r'\d+', obj.name)))[0]

def make_object_voxel(vox_array, voxel_object): 
    collection_name = "VoxelCollection"

    # Check if the collection already exists
    if collection_name in bpy.data.collections:
        objects = sorted(bpy.data.collections['VoxelCollection'].all_objects, key=num_sort)
        
        for x in range(len(vox_array)):
            for y in range(len(vox_array[x])):
                for z in range(len(vox_array[x][y])):
                    if (vox_array[x][y][z] != 0) and (vox_array[x][y][z] <= len(objects)):
                        me = objects[int(vox_array[x][y][z]) - 1].data #mesh of obj
                        obj = bpy.data.objects.new('Duplicate_Linked', me)
                        bpy.context.scene.collection.objects.link(obj)
                        tmp = obj.location
                        obj.location = mathutils.Vector((x, y, z)) #get position in obj space
                        obj.parent = voxel_object
    else:
        # Create a new collection
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
        print(f"put objects to be instanced in'{collection_name}'. order in outliner is voxel order.")
    
    