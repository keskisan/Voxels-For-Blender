import bpy
import bmesh
import numpy as np
import mathutils
import math
import  bpy_extras
from bpy_extras import view3d_utils #this library is idiosyncratic

import sys
import os

import re

def get_matx_maty(voxel_menu_var, uv_scale, mat_num):
    num = mat_num - 1
    mat_x = (num % voxel_menu_var.voxel_uv_scale)*uv_scale #x offset
    mat_y = (math.floor(num / voxel_menu_var.voxel_uv_scale))*uv_scale #yoffset
    return (mat_x, mat_y)


def calculate_hex_smooth_array(smooth_array, vox_array):
     #populate a new array with the average off all the voxel smooth types according to the voxel array number(type)
    vertex_smooth_count = np.zeros((math.floor(len(vox_array)/2 + 1), len(vox_array[1]) + 1, len(vox_array[1][1]) + 1)) #x is only half as 2 triangles to a square
    vertex_smooth_array = np.full((len(vertex_smooth_count), len(vertex_smooth_count[1]), len(vertex_smooth_count[1][1])), -1000.55) #less than -100 considered empty
    
    for x in range(len(vertex_smooth_count) - 1): 
        for y in range(len(vertex_smooth_count[x]) - 1):
            for z in range(len(vertex_smooth_count[x][y]) - 1):
                if x * 2 < len(vox_array):
                    if vox_array[x][y][z] >= len(smooth_array): #vallue can be set to anything even outside array
                        smoothfactor = 0
                    else:
                        smoothfactor = smooth_array[int(vox_array[x][y][z])] 
                    
                    #if x % 2 == 0:
                    #    if y % 2 == 0:
                    #function currently written run four at time but run each act so innefecient
                    
                    if vox_array[x * 2][y][z] > 0: #00
                        if vertex_smooth_array[x][y][z] < -100:
                            vertex_smooth_array[x][y][z] = smoothfactor
                        else:
                           vertex_smooth_array[x][y][z] = vertex_smooth_array[x][y][z] +  smoothfactor
                        vertex_smooth_count[x][y][z] += 1
                        
                        if vertex_smooth_array[x + 1][y][z] < -100:
                            vertex_smooth_array[x + 1][y][z] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y][z] = vertex_smooth_array[x + 1][y][z] +  smoothfactor
                        vertex_smooth_count[x + 1][y][z] += 1
                        
                        if vertex_smooth_array[x][y + 1][z] < -100:
                            vertex_smooth_array[x][y + 1][z] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z] = vertex_smooth_array[x][y + 1][z] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z] += 1
                        
                        
                        if vertex_smooth_array[x][y][z + 1] < -100:
                            vertex_smooth_array[x][y][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x][y][z + 1] = vertex_smooth_array[x][y][z + 1] +  smoothfactor
                        vertex_smooth_count[x][y][z + 1] += 1
                        
                        if vertex_smooth_array[x + 1][y][z + 1] < -100:
                            vertex_smooth_array[x + 1][y][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y][z + 1] = vertex_smooth_array[x + 1][y][z + 1] + smoothfactor
                        vertex_smooth_count[x + 1][y][z + 1] += 1
                        
                        if vertex_smooth_array[x][y + 1][z + 1] < -100:
                            vertex_smooth_array[x][y + 1][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z + 1] = vertex_smooth_array[x][y + 1][z + 1] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z + 1] += 1
                    
                    
                if x * 2 + 1 < len(vox_array):    
                    if vox_array[x*2 + 1][y][z] > 0:        #10         
                        if vertex_smooth_array[x + 1][y][z] < -100:
                            vertex_smooth_array[x + 1][y][z] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y][z] = vertex_smooth_array[x + 1][y][z] +  smoothfactor
                        vertex_smooth_count[x + 1][y][z] += 1
                        
                        if vertex_smooth_array[x][y + 1][z] < -100:
                            vertex_smooth_array[x][y + 1][z] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z] = vertex_smooth_array[x][y + 1][z] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z] += 1
                        
                        if vertex_smooth_array[x + 1][y + 1][z] < -100:
                            vertex_smooth_array[x + 1][y + 1][z] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 1][z] = vertex_smooth_array[x + 1][y + 1][z] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 1][z] += 1
                        
                        
                        if vertex_smooth_array[x + 1][y][z + 1] < -100:
                            vertex_smooth_array[x + 1][y][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y][z + 1] = vertex_smooth_array[x + 1][y][z + 1] +  smoothfactor
                        vertex_smooth_count[x + 1][y][z + 1] += 1
                        
                        if vertex_smooth_array[x][y + 1][z + 1] < -100:
                            vertex_smooth_array[x][y + 1][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z + 1] = vertex_smooth_array[x][y + 1][z + 1] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z + 1] += 1
                        
                        if vertex_smooth_array[x + 1][y + 1][z + 1] < -100:
                            vertex_smooth_array[x + 1][y + 1][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 1][z + 1] = vertex_smooth_array[x + 1][y + 1][z + 1] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 1][z + 1] += 1
                    
                    
                if x * 2 < len(vox_array) and y + 1 < len(vox_array[1]):    
                    if vox_array[x*2][y + 1][z] > 0: #01
                        if vertex_smooth_array[x][y + 1][z] < -100:
                            vertex_smooth_array[x][y + 1][z] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z] = vertex_smooth_array[x][y + 1][z] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z] += 1
                        
                        if vertex_smooth_array[x][y + 2][z] < -100:
                            vertex_smooth_array[x][y + 2][z] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 2][z] = vertex_smooth_array[x][y + 2][z] +  smoothfactor
                        vertex_smooth_count[x][y + 2][z] += 1
                        
                        if vertex_smooth_array[x + 1][y + 2][z] < -100:
                            vertex_smooth_array[x + 1][y + 2][z] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 2][z] = vertex_smooth_array[x + 1][y + 2][z] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 2][z] += 1
                        
                        
                        if vertex_smooth_array[x][y + 1][z + 1] < -100:
                            vertex_smooth_array[x][y + 1][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z + 1] = vertex_smooth_array[x][y + 1][z + 1] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z + 1] += 1
                        
                        if vertex_smooth_array[x][y + 2][z + 1] < -100:
                            vertex_smooth_array[x][y + 2][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 2][z + 1] = vertex_smooth_array[x][y + 2][z + 1] +  smoothfactor
                        vertex_smooth_count[x][y + 2][z + 1] += 1
                        
                        if vertex_smooth_array[x + 1][y + 2][z + 1] < -100:
                            vertex_smooth_array[x + 1][y + 2][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 2][z + 1] = vertex_smooth_array[x + 1][y + 2][z + 1] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 2][z + 1] += 1
                    
                    
                if x * 2 + 1 < len(vox_array) and y + 1 < len(vox_array[1]):    
                    if vox_array[x*2 + 1][y + 1][z] > 0: #11
                        if vertex_smooth_array[x][y + 1][z] < -100:
                            vertex_smooth_array[x][y + 1][z] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z] = vertex_smooth_array[x][y + 1][z] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z] += 1
                        
                        if vertex_smooth_array[x + 1][y + 2][z] < -100:
                            vertex_smooth_array[x + 1][y + 2][z] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 2][z] = vertex_smooth_array[x + 1][y + 2][z] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 2][z] += 1
                        
                        if vertex_smooth_array[x + 1][y + 1][z] < -100:
                            vertex_smooth_array[x + 1][y + 1][z] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 2][z] = vertex_smooth_array[x + 1][y + 2][z] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 2][z] += 1
                        
                        
                        if vertex_smooth_array[x][y + 1][z + 1] < -100:
                            vertex_smooth_array[x][y + 1][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x][y + 1][z + 1] = vertex_smooth_array[x][y + 1][z + 1] +  smoothfactor
                        vertex_smooth_count[x][y + 1][z + 1] += 1
                        
                        if vertex_smooth_array[x + 1][y + 2][z + 1] < -100:
                            vertex_smooth_array[x + 1][y + 2][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 2][z + 1] = vertex_smooth_array[x + 1][y + 2][z + 1] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 2][z + 1] += 1
                        
                        if vertex_smooth_array[x + 1][y + 1][z + 1] < -100:
                            vertex_smooth_array[x + 1][y + 1][z + 1] = smoothfactor
                        else:
                           vertex_smooth_array[x + 1][y + 2][z + 1] = vertex_smooth_array[x + 1][y + 2][z + 1] +  smoothfactor
                        vertex_smooth_count[x + 1][y + 2][z + 1] += 1
                    
                    
                    
                    
    for x in range(len(vertex_smooth_array)):
        for y in range(len(vertex_smooth_array[x])):
            for z in range(len(vertex_smooth_array[x][y])):                
                vertex_smooth_array[x][y][z] = vertex_smooth_array[x][y][z]/vertex_smooth_count[x][y][z]
                
    return vertex_smooth_array



def get_vertex_array_offset_hex(vertex_smooth_array, x, y, z):
    #calculate offsets
    x_offset = 0
    y_offset = 0
    z_offset = 0
    x_half = math.floor(x/2)
    if x_half >= len(vertex_smooth_array) - 1:
        x_half = len(vertex_smooth_array) - 1
        
    if x_half > 0:
        if vertex_smooth_array[x_half - 1][y][z] > -100:
            x_offset -= vertex_smooth_array[x_half - 1][y][z]
    if x_half < len(vertex_smooth_array) - 1:
        if vertex_smooth_array[x_half + 1][y][z] > -100:
            x_offset += vertex_smooth_array[x_half + 1][y][z]
           
    if y % 2 == 0: #even
        if y > 0:
            if vertex_smooth_array[x_half][y - 1][z] > -100:
                y_offset -= vertex_smooth_array[x_half][y - 1][z]
                x_offset += vertex_smooth_array[x_half][y - 1][z]
            if x_half > 0:
                if vertex_smooth_array[x_half - 1][y - 1][z] > -100:
                    y_offset -= vertex_smooth_array[x_half - 1][y - 1][z]
                    x_offset -= vertex_smooth_array[x_half - 1][y - 1][z]
                    
        if y < len(vertex_smooth_array[1]) - 1:
            if vertex_smooth_array[x_half][y + 1][z] > -100:
                y_offset += vertex_smooth_array[x_half][y + 1][z]
                x_offset += vertex_smooth_array[x_half][y + 1][z]
            if x_half > 0:
                if vertex_smooth_array[x_half - 1][y + 1][z] > -100:
                    y_offset += vertex_smooth_array[x_half - 1][y + 1][z]
                    x_offset -= vertex_smooth_array[x_half - 1][y + 1][z]
                
    else: #odd
        if y > 0:
            if vertex_smooth_array[x_half][y - 1][z] > -100:
                y_offset -= vertex_smooth_array[x_half][y - 1][z]
                x_offset -= vertex_smooth_array[x_half][y - 1][z]
            if x_half < len(vertex_smooth_array) - 1:
                if vertex_smooth_array[x_half + 1][y - 1][z] > -100:
                    y_offset -= vertex_smooth_array[x_half + 1][y - 1][z]
                    x_offset += vertex_smooth_array[x_half + 1][y - 1][z]
          
                
        if y < len(vertex_smooth_array[1]) - 1:
            if vertex_smooth_array[x_half][y + 1][z] > -100:
                y_offset += vertex_smooth_array[x_half][y + 1][z]
                x_offset -= vertex_smooth_array[x_half][y + 1][z]
            if x_half < len(vertex_smooth_array) - 1:
                if vertex_smooth_array[x_half + 1][y + 1][z] > -100:
                    y_offset += vertex_smooth_array[x_half + 1][y + 1][z]
                    x_offset += vertex_smooth_array[x_half + 1][y + 1][z]
        
     
            
          
    if z > 0:
        if vertex_smooth_array[x_half][y][z - 1] > -100:
            z_offset -= vertex_smooth_array[x_half][y][z - 1] 
    if z < len(vertex_smooth_array[1][1]) - 1:
        if vertex_smooth_array[x_half][y][z + 1] > -100:
            z_offset += vertex_smooth_array[x_half][y][z + 1]
   
            
    #return final position
    return (x + x_offset, y + y_offset, z + z_offset)



def add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w,):

    vert_coords.append(get_vertex_array_offset_hex(vertex_smooth_array, a[0] + x, a[1] + y, a[2] + z))
    vert_coords.append(get_vertex_array_offset_hex(vertex_smooth_array, b[0] + x, b[1] + y, b[2] + z))
    vert_coords.append(get_vertex_array_offset_hex(vertex_smooth_array, c[0] + x, c[1] + y, c[2] + z))
    
    length = len(vert_coords)
    
    face_vert_indices.append ((length - 3, length - 2, length - 1))
    
    
    uv_loop = [u ,v, w]
  
    uvs.append(uv_loop)

def add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w):

    vert_coords.append(get_vertex_array_offset_hex(vertex_smooth_array, a[0] + x, a[1] + y, a[2] + z))
    vert_coords.append(get_vertex_array_offset_hex(vertex_smooth_array, b[0] + x, b[1] + y, b[2] + z))
    vert_coords.append(get_vertex_array_offset_hex(vertex_smooth_array, c[0] + x, c[1] + y, c[2] + z))
    vert_coords.append(get_vertex_array_offset_hex(vertex_smooth_array, d[0] + x, d[1] + y, d[2] + z))
    
    length = len(vert_coords)
    
    face_vert_indices.append ((length - 4, length - 3, length - 2, length - 1))
    
    
    uv_loop = [t, u, v, w]
  
    uvs.append(uv_loop)

def generate_hex_prism_voxels(vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, uv_scale, bufferx, buffery, vertex_smooth_array):
    for x in range(len(vox_array)):
        for y in range(len(vox_array[x])):
            for z in range(len(vox_array[x][y])): 
                if (vox_array[x][y][z] != 0):
                    mat_x, mat_y = get_matx_maty(voxel_menu_var, uv_scale, vox_array[x][y][z])       
                    if x % 2 == 0:
                        if y % 2 == 0: 
                            if z > 0:
                                if vox_array[x][y][z - 1] == 0:
                                    a = np.array([0, 0, 0])
                                    b = np.array([1, 1, 0])   
                                    c = np.array([2, 0, 0])
                                    u = (mat_x + bufferx, mat_y + buffery) #(0, 0)
                                    v = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                    w = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            else:  
                                a = np.array([0, 0, 0])
                                b = np.array([1, 1, 0])   
                                c = np.array([2, 0, 0])
                                u = (mat_x + bufferx, mat_y + buffery) #(0, 0)
                                v = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                w = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            
                            if z < len(vox_array[x][y]) - 1:
                                if vox_array[x][y][z + 1] == 0:
                                    a = np.array([1, 1, 1])   
                                    b = np.array([0, 0, 1])
                                    c = np.array([2, 0, 1])
                                    u = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 + buffery) #(0, 0)
                                    w = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            else:
                                a = np.array([1, 1, 1])   
                                b = np.array([0, 0, 1])
                                c = np.array([2, 0, 1])
                                u = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 + buffery) #(0, 0)
                                w = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            
                            
                            if x > 0:
                                if vox_array[x - 1][y][z] == 0:
                                    a = np.array([1, 1, 0])   
                                    b = np.array([0, 0, 0])
                                    c = np.array([0, 0, 1])
                                    d = np.array([1, 1, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([1, 1, 0])   
                                b = np.array([0, 0, 0])
                                c = np.array([0, 0, 1])
                                d = np.array([1, 1, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                                
                            if y > 0:
                                if vox_array[x][y - 1][z] == 0:
                                    a = np.array([0, 0, 0])
                                    b = np.array([2, 0, 0])   
                                    c = np.array([2, 0, 1])
                                    d = np.array([0, 0, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([0, 0, 0])
                                b = np.array([2, 0, 0])   
                                c = np.array([2, 0, 1])
                                d = np.array([0, 0, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            
                            if x < len(vox_array) - 1:
                                if vox_array[x + 1][y][z] == 0:
                                    a = np.array([2, 0, 0])   
                                    b = np.array([1, 1, 0])
                                    c = np.array([1, 1, 1])
                                    d = np.array([2, 0, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)       
                            else:
                                a = np.array([2, 0, 0])   
                                b = np.array([1, 1, 0])
                                c = np.array([1, 1, 1])
                                d = np.array([2, 0, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            
                        else: #eeeeeeeeeeeeeeee
                            if z > 0:
                                if vox_array[x][y][z - 1] == 0:
                                    a = np.array([1, 0, 0])
                                    b = np.array([0, 1, 0])   
                                    c = np.array([2, 1, 0])
                                    u = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                    v = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 - buffery) #(1, 1)
                                    w = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)  
                            else:
                                a = np.array([1, 0, 0])
                                b = np.array([0, 1, 0])   
                                c = np.array([2, 1, 0])
                                u = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                v = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 - buffery) #(1, 1)
                                w = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)  
                            
                            if z < len(vox_array[x][y]) - 1:
                                if vox_array[x][y][z + 1] == 0:    
                                    a = np.array([0, 1, 1])
                                    b = np.array([1, 0, 1])   
                                    c = np.array([2, 1, 1])
                                    u = (mat_x + uv_scale - bufferx, mat_y + uv_scale - buffery) #(1, 1)
                                    v = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                    w = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)  
                            else:
                                a = np.array([0, 1, 1])
                                b = np.array([1, 0, 1])   
                                c = np.array([2, 1, 1])
                                u = (mat_x + uv_scale - bufferx, mat_y + uv_scale - buffery) #(1, 1)
                                v = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                w = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)  
                                
                            if x > 0:
                                if vox_array[x - 1][y][z] == 0:
                                    a = np.array([0, 1, 0])   
                                    b = np.array([1, 0, 0])
                                    c = np.array([1, 0, 1])
                                    d = np.array([0, 1, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([0, 1, 0])   
                                b = np.array([1, 0, 0])
                                c = np.array([1, 0, 1])
                                d = np.array([0, 1, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            
                            if x < len(vox_array) - 1:
                                if vox_array[x + 1][y][z] == 0: 
                                    a = np.array([1, 0, 0])
                                    b = np.array([2, 1, 0])   
                                    c = np.array([2, 1, 1])
                                    d = np.array([1, 0, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([1, 0, 0])
                                b = np.array([2, 1, 0])   
                                c = np.array([2, 1, 1])
                                d = np.array([1, 0, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            
                            if y < len(vox_array) - 1:
                                if vox_array[x][y + 1][z] == 0:
                                    a = np.array([2, 1, 0])   
                                    b = np.array([0, 1, 0])
                                    c = np.array([0, 1, 1])
                                    d = np.array([2, 1, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([2, 1, 0])   
                                b = np.array([0, 1, 0])
                                c = np.array([0, 1, 1])
                                d = np.array([2, 1, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            
                    else: #eeeeeeeeeeeeeeeeeeeeee
                        if y % 2 == 0: 
                            if z > 0:
                                if vox_array[x][y][z - 1] == 0:
                                    a = np.array([0, 1, 0])  
                                    c = np.array([1, 0, 0]) 
                                    b = np.array([2, 1, 0])
                                    u = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 - buffery) #(1, 1)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            else:
                                a = np.array([0, 1, 0])  
                                c = np.array([1, 0, 0]) 
                                b = np.array([2, 1, 0])
                                u = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 - buffery) #(1, 1)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            
                            if z < len(vox_array[x][y]) - 1:
                                if vox_array[x][y][z + 1] == 0:
                                    a = np.array([1, 0, 1])  
                                    c = np.array([0, 1, 1]) 
                                    b = np.array([2, 1, 1])
                                    u = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale - buffery) #(1, 1)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            else:
                                a = np.array([1, 0, 1])  
                                c = np.array([0, 1, 1]) 
                                b = np.array([2, 1, 1])
                                u = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale - buffery) #(1, 1)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                                
                            if x > 0:
                                if vox_array[x - 1][y][z] == 0:
                                    a = np.array([0, 1, 0])   
                                    b = np.array([1, 0, 0])
                                    c = np.array([1, 0, 1])
                                    d = np.array([0, 1, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([0, 1, 0])   
                                b = np.array([1, 0, 0])
                                c = np.array([1, 0, 1])
                                d = np.array([0, 1, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                           
                            if y < len(vox_array[x]) - 1:
                                if vox_array[x][y + 1][z] == 0:
                                    a = np.array([2, 1, 0])
                                    b = np.array([0, 1, 0])   
                                    c = np.array([0, 1, 1])
                                    d = np.array([2, 1, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([2, 1, 0])
                                b = np.array([0, 1, 0])   
                                c = np.array([0, 1, 1])
                                d = np.array([2, 1, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            
                            if x < len(vox_array) - 1:
                                if vox_array[x + 1][y][z] == 0:
                                    a = np.array([1, 0, 0])   
                                    b = np.array([2, 1, 0])
                                    c = np.array([2, 1, 1])
                                    d = np.array([1, 0, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([1, 0, 0])   
                                b = np.array([2, 1, 0])
                                c = np.array([2, 1, 1])
                                d = np.array([1, 0, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                           
                        else: #eeeeeeeeeeeeeeeeeeeee
                            if z > 0:
                                if vox_array[x][y][z - 1] == 0:
                                    a = np.array([0, 0, 0])   
                                    b = np.array([1, 1, 0])
                                    c = np.array([2, 0, 0])
                                    u = (mat_x + bufferx, mat_y + buffery) #(0, 0)
                                    v = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                    w = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                            else:
                                a = np.array([0, 0, 0])   
                                b = np.array([1, 1, 0])
                                c = np.array([2, 0, 0])
                                u = (mat_x + bufferx, mat_y + buffery) #(0, 0)
                                v = (mat_x + uv_scale - bufferx, mat_y + buffery) #(1, 0)
                                w = (mat_x + bufferx, mat_y + uv_scale*0.33 - buffery) #(0, 1)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)    
                               
                            if z < len(vox_array[x][y]) - 1:
                                if vox_array[x][y][z + 1] == 0: 
                                    a = np.array([1, 1, 1])   
                                    b = np.array([0, 0, 1])
                                    c = np.array([2, 0, 1])
                                    v = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                    w = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                    u = (mat_x + bufferx, mat_y + uv_scale*0.66 + buffery) #(0, 0)
                                    add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)   
                            else:
                                a = np.array([1, 1, 1])   
                                b = np.array([0, 0, 1])
                                c = np.array([2, 0, 1])
                                v = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 + buffery) #(1, 0)
                                w = (mat_x + bufferx, mat_y + uv_scale - buffery) #(0, 1)
                                u = (mat_x + bufferx, mat_y + uv_scale*0.66 + buffery) #(0, 0)
                                add_triangle_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, x, y, z, uvs, u, v, w)
                                
                            if x > 0:
                                if vox_array[x - 1][y][z] == 0:    
                                    a = np.array([1, 1, 0])   
                                    b = np.array([0, 0, 0])
                                    c = np.array([0, 0, 1])
                                    d = np.array([1, 1, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([1, 1, 0])   
                                b = np.array([0, 0, 0])
                                c = np.array([0, 0, 1])
                                d = np.array([1, 1, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                                
                            if y > 0:
                                if vox_array[x][y - 1][z] == 0:
                                    a = np.array([0, 0, 0])
                                    b = np.array([2, 0, 0])   
                                    c = np.array([2, 0, 1])
                                    d = np.array([0, 0, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([0, 0, 0])
                                b = np.array([2, 0, 0])   
                                c = np.array([2, 0, 1])
                                d = np.array([0, 0, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            
                            if x < len(vox_array) - 1:
                                if vox_array[x + 1][y][z] == 0: 
                                    a = np.array([2, 0, 0])   
                                    b = np.array([1, 1, 0])
                                    c = np.array([1, 1, 1])
                                    d = np.array([2, 0, 1])
                                    t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                    u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                    v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                    w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                    add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                            else:
                                a = np.array([2, 0, 0])   
                                b = np.array([1, 1, 0])
                                c = np.array([1, 1, 1])
                                d = np.array([2, 0, 1])
                                t = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.33 + buffery) #(1, 0)
                                u = (mat_x +  bufferx, mat_y + uv_scale*0.33 + buffery) #(0, 0)
                                v = (mat_x + bufferx, mat_y + uv_scale*0.66 - buffery) #(0, 1)
                                w = (mat_x + uv_scale - bufferx, mat_y + uv_scale*0.66 - buffery) #(1, 1)
                                add_quad_hex(vertex_smooth_array, voxel_menu_var, vert_coords, face_vert_indices, a, b, c, d, x, y, z, uvs, t, u, v, w)
                

