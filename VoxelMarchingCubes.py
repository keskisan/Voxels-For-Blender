import bpy
import bmesh
import numpy as np
import mathutils
import math

import sys
import os
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    

import marching_cubes_table as MCT

import imp
imp.reload(MCT)

def get_matx_maty(voxel_menu_var, uv_scale, mat_num):
    num = mat_num - 1
    mat_x = (num % voxel_menu_var.voxel_uv_scale)*uv_scale #x offset
    mat_y = (math.floor(num / voxel_menu_var.voxel_uv_scale))*uv_scale #yoffset
    return (mat_x, mat_y)

def add_triangle(voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, uv_scale, uv_scale3, mat_num):

    vert_coords.append((a[0] + x, a[1] + y, a[2] + z))
    vert_coords.append((b[0] + x, b[1] + y, b[2] + z))
    vert_coords.append((c[0] + x, c[1] + y, c[2] + z))
    
    length = len(vert_coords)
    
    face_vert_indices.append ((length - 3, length - 2, length - 1))
    
    
    #uvs
    matx, maty = get_matx_maty(voxel_menu_var, uv_scale, mat_num)
    
    sub1 = mathutils.Vector(b - a)
    sub2 = mathutils.Vector(b - c)
    
    norm = sub1.cross(sub2).normalized()
    
    xdir = mathutils.Vector([1,0,0])
    ydir = mathutils.Vector([0,1,0])
    zdir = mathutils.Vector([0,0,1])
    
    dotX = abs(norm.dot(xdir))
    dotY = abs(norm.dot(ydir))
    dotZdir = norm.dot(zdir)
    dotZ = abs(dotZdir)
    
    if (dotZdir > voxel_menu_var.voxel_bottomCover): #top
            uv_loop = [(a[0] * uv_scale + matx, a[1] * uv_scale3 + maty), (b[0] * uv_scale + matx, b[1] * uv_scale3 + maty), (c[0] * uv_scale + matx,  c[1] * uv_scale3 + maty)]
    elif(dotZdir < voxel_menu_var.voxel_topCover):  #bottom
            uv_loop = [(a[0] * uv_scale + matx, a[1] * uv_scale3 + uv_scale3*2 + maty), (b[0] * uv_scale + matx, b[1] * uv_scale3 + uv_scale3*2 + maty), (c[0] * uv_scale + matx,  c[1] * uv_scale3 + uv_scale3*2 + maty)] 
    elif (dotX >= dotY):
        uv_loop = [(a[1] * uv_scale + matx, a[2] * uv_scale3 + uv_scale3 + maty), (b[1] * uv_scale + matx, b[2] * uv_scale3 + uv_scale3 + maty), (c[1] * uv_scale + matx,  c[2] * uv_scale3 + uv_scale3 + maty)]
    elif (dotY >= dotX ):
        uv_loop = [(a[0] * uv_scale + matx, a[2] * uv_scale3 + uv_scale3 + maty), (b[0] * uv_scale + matx, b[2] * uv_scale3 + uv_scale3 + maty), (c[0] * uv_scale + matx,  c[2] * uv_scale3 + uv_scale3 + maty)]
  
    uvs.append(uv_loop)



def generate_marching_cubes_voxels(smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, uv_scale, uv_scale3):
    #marching
    for x in range(len(vox_array)):
        for y in range(len(vox_array[x])):
            for z in range(len(vox_array[x][y])):
                
                #touch edges
                x_min = False
                x_max = False
                y_min = False
                y_max = False
                z_min = False
                z_max = False
                if x == 0:
                    x_min = True
                elif x == len(vox_array) - 1:
                    x_max = True
                if y == 0:
                    y_min = True
                elif y == len(vox_array[x]) - 1:
                    y_max = True
                if z == 0:
                    z_min = True
                elif z == len(vox_array[x][y]) - 1:
                    z_max = True
                    
                     
                #get tri_table index
                cube_index = 0; 
               

                if x_min or y_min or z_max: 
                    cube_index += 1
                else:
                    if vox_array[x][y][z  + 1] == 0:
                        cube_index += 1    
                         
                if x_max or y_min or z_max: 
                    cube_index += 2
                else:
                    if vox_array[x  + 1][y][z  + 1] == 0:
                        cube_index += 2
                    
                if x_max or y_min or z_min:  
                    cube_index += 4
                else:
                    if vox_array[x  + 1][y][z] == 0:
                        cube_index += 4
                    
                if x_min or y_min or z_min: 
                    cube_index += 8;
                else:
                    if vox_array[x][y][z] == 0: 
                        cube_index += 8
                        
                if x_min or y_max or z_max:  
                    cube_index += 16;
                else:
                    if vox_array[x][y  + 1][z  + 1] == 0:  
                        cube_index += 16;
                        
                if x_max or y_max or z_max:  
                    cube_index += 32;
                else:
                    if vox_array[x  + 1][y  + 1][z  + 1] == 0:  
                     cube_index += 32;
                    
                if x_max or y_max or z_min: 
                    cube_index += 64;
                else:
                    if vox_array[x  + 1][y  + 1][z] == 0: 
                        cube_index += 64;
                        
                if x_min or y_max or z_min: 
                    cube_index += 128;
                else:
                    if vox_array[x][y  + 1][z] == 0: 
                        cube_index += 128;
                    
                              
                edges = MCT.tri_table[cube_index];
                
                for i in range(0, len(edges), 3):
                    if edges[i] == -1:
                        break
                    #edge 1 lies between vertex e00 and e01
                    e00 =  MCT.edge_onnections[edges[i]][0];
                    e01 =  MCT.edge_onnections[edges[i]][1];
                    
                    #edge 2 lies between vertex e10 and e11
                    e10 =  MCT.edge_onnections[edges[i + 1]][0];
                    e11 =  MCT.edge_onnections[edges[i + 1]][1];
                    
                    #edge 3  lies between vertex e20 and e21
                    e20 =  MCT.edge_onnections[edges[i + 2]][0];
                    e21 =  MCT.edge_onnections[edges[i + 2]][1];
                    
                    a = (MCT.corner_offsets[e00] +  MCT.corner_offsets[e01]) / 2;
                    b = (MCT.corner_offsets[e10] +  MCT.corner_offsets[e11]) / 2;
                    c = (MCT.corner_offsets[e20] +  MCT.corner_offsets[e21]) / 2;
                    
                    
                    #theres a bug here so ugly still buggy
                    vox_content_num = 0;
                    if vox_array[x][y][z] != 0:
                        vox_content_num = vox_array[x][y][z]
                    if x_max == False:
                        if vox_array[x + 1][y][z] != 0:
                            vox_content_num = vox_array[x + 1][y][z]
                    if y_max == False:
                        if vox_array[x][y + 1][z] != 0:
                            vox_content_num = vox_array[x][y + 1][z]
                    if x_max  == False and y_max == False:
                        if vox_array[x + 1][y + 1][z] != 0:
                            vox_content_num = vox_array[x + 1][y + 1][z]
                    if z_max == False:
                        if vox_array[x][y][z + 1] != 0:
                            vox_content_num = vox_array[x][y][z + 1]
                    if x_max  == False and z_max  == False:
                        if vox_array[x + 1][y][z + 1] != 0:
                            vox_content_num = vox_array[x + 1][y][z + 1]
                    if y_max  == False and z_max  == False:
                        if vox_array[x][y + 1][z + 1] != 0:
                            vox_content_num = vox_array[x][y + 1][z + 1]
                    if x_max  == False and y_max  == False and z_max == False:
                        if vox_array[x + 1][y + 1][z + 1] != 0:
                            vox_content_num = vox_array[x + 1][y + 1][z + 1]
                   
                    
                    
                    add_triangle(voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, uv_scale, uv_scale3, vox_content_num);