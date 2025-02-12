import bpy
import bmesh
import numpy as np
import mathutils
import math



def get_vertex_array_offset(vertex_smooth_array, x, y, z):
    #calculate offsets
    x_offset = 0
    if x > 0:
        if vertex_smooth_array[x - 1][y][z] > -100:
            x_offset -= vertex_smooth_array[x - 1][y][z]
    if x < len(vertex_smooth_array) - 1:
        if vertex_smooth_array[x + 1][y][z] > -100:
            x_offset += vertex_smooth_array[x + 1][y][z]
      
    y_offset = 0      
    if y > 0:
        if vertex_smooth_array[x][y - 1][z] > -100:
            y_offset -= vertex_smooth_array[x][y - 1][z]
    if y < len(vertex_smooth_array[1]) - 1:
        if vertex_smooth_array[x][y + 1][z] > -100:
            y_offset += vertex_smooth_array[x][y + 1][z]
            
    z_offset = 0      
    if z > 0:
        if vertex_smooth_array[x][y][z - 1] > -100:
            z_offset -= vertex_smooth_array[x][y][z - 1]
    if z < len(vertex_smooth_array[1][1]) - 1:
        if vertex_smooth_array[x][y][z + 1] > -100:
            z_offset += vertex_smooth_array[x][y][z + 1]
            
    #return final position
    return (x + x_offset, y + y_offset, z + z_offset)
        
        
            
def get_matx_maty(voxel_menu_var, uv_scale, mat_num):
    num = mat_num - 1
    mat_x = (num % voxel_menu_var.voxel_uv_scale)*uv_scale #x offset
    mat_y = (math.floor(num / voxel_menu_var.voxel_uv_scale))*uv_scale #yoffset
    return (mat_x, mat_y)


def add_ypos_face(vertex_smooth_array, voxel_menu_var, pos_x, pos_y, pox_z, vert_coords, face_vert_indices, uvs, uv_scale, mat_num, bufferx, buffery):
    
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 1 + pos_y, 1 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 1 + pos_y, 1 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 1 + pos_y, 0 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 1 + pos_y, 0 + pox_z))
    
    length = len(vert_coords)
    
    face_vert_indices.append (( length - 4, length - 3, length - 2, length - 1))
    
    
    mat_x, mat_y = get_matx_maty(voxel_menu_var, uv_scale, mat_num)
    
    uv_loop = [(uv_scale + mat_x - bufferx, uv_scale*0.66  + mat_y - buffery), (mat_x + bufferx, uv_scale*0.66  + mat_y - buffery), (mat_x + bufferx, uv_scale*0.33  + mat_y + buffery), (uv_scale  + mat_x - bufferx, uv_scale*0.33  + mat_y + buffery)]
    uvs.append(uv_loop)
    
 
 
def add_yneg_face(vertex_smooth_array, voxel_menu_var, pos_x, pos_y, pox_z, vert_coords, face_vert_indices, uvs, uv_scale, mat_num, bufferx, buffery):

    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 0 + pos_y, 0 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 0 + pos_y, 1 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 0 + pos_y, 1 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 0 + pos_y, 0 + pox_z))
    
    length = len(vert_coords)
    
    face_vert_indices.append (( length - 4, length - 3, length - 2, length - 1))  
    
    
    mat_x, mat_y = get_matx_maty(voxel_menu_var, uv_scale, mat_num)
    
    uv_loop = [(uv_scale + mat_x - bufferx, uv_scale*0.33 + mat_y + buffery), (uv_scale + mat_x - bufferx, uv_scale*0.66 + mat_y - buffery), (mat_x + bufferx, uv_scale*0.66 + mat_y - buffery), (mat_x + bufferx, uv_scale*0.33 + mat_y + buffery)]
    uvs.append(uv_loop)
     


def add_xneg_face(vertex_smooth_array, voxel_menu_var, pos_x, pos_y, pox_z, vert_coords, face_vert_indices, uvs, uv_scale, mat_num, bufferx, buffery):

    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 0 + pos_y, 0 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 0 + pos_y, 1 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 1 + pos_y, 1 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 1 + pos_y, 0 + pox_z))
    
    length = len(vert_coords)
    
    face_vert_indices.append (( length - 4, length - 3, length - 2, length - 1))   
    
    
    mat_x, mat_y = get_matx_maty(voxel_menu_var, uv_scale, mat_num)
    
    uv_loop = [(uv_scale + mat_x - bufferx, uv_scale*0.33 + mat_y + buffery), (uv_scale + mat_x - bufferx, uv_scale*0.66 + mat_y - buffery), (mat_x + bufferx, uv_scale*0.66 + mat_y - buffery), (mat_x + bufferx, uv_scale*0.33 + mat_y + buffery)]
    uvs.append(uv_loop)



def add_xpos_face(vertex_smooth_array, voxel_menu_var, pos_x, pos_y, pox_z, vert_coords, face_vert_indices, uvs, uv_scale, mat_num, bufferx, buffery):

    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 1 + pos_y, 0 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 1 + pos_y, 1 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 0 + pos_y, 1 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 0 + pos_y, 0 + pox_z))
    
    length = len(vert_coords)
    
    face_vert_indices.append (( length - 4, length - 3, length - 2, length - 1))   
    
    
    mat_x, mat_y = get_matx_maty(voxel_menu_var, uv_scale, mat_num)
    
    uv_loop = [(uv_scale + mat_x - bufferx, uv_scale*0.33 + mat_y + buffery), (uv_scale + mat_x - bufferx, uv_scale*0.66 + mat_y - buffery), (mat_x + bufferx, uv_scale*0.66 + mat_y - buffery), (mat_x + bufferx, uv_scale*0.33 + mat_y + buffery)]
    uvs.append(uv_loop)



def add_zneg_face(vertex_smooth_array, voxel_menu_var, pos_x, pos_y, pox_z, vert_coords, face_vert_indices, uvs, uv_scale, mat_num, bufferx, buffery):

    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 1 + pos_y, 0 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 1 + pos_y, 0 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 0 + pos_y, 0 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 0 + pos_y, 0 + pox_z))
    
    length = len(vert_coords)
    
    face_vert_indices.append (( length - 4, length - 3, length - 2, length - 1)) 
    
    
    mat_x, mat_y = get_matx_maty(voxel_menu_var, uv_scale, mat_num)
    
    uv_loop = [(uv_scale + mat_x - bufferx, uv_scale*0.33 + mat_y - buffery), (mat_x + bufferx, uv_scale*0.33 + mat_y - buffery), (mat_x + bufferx,  mat_y + buffery), (uv_scale + mat_x - bufferx,  mat_y + buffery)]
    uvs.append(uv_loop)
    
    
    
def add_zpos_face(vertex_smooth_array, voxel_menu_var, pos_x, pos_y, pox_z, vert_coords, face_vert_indices, uvs, uv_scale, mat_num, bufferx, buffery):

    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 0 + pos_y, 1 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 0 + pos_y, 1 + pox_z))
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 1 + pos_x, 1 + pos_y, 1 + pox_z)) 
    vert_coords.append(get_vertex_array_offset(vertex_smooth_array, 0 + pos_x, 1 + pos_y, 1 + pox_z))  
    
    length = len(vert_coords)
    
    face_vert_indices.append (( length - 4, length - 3, length - 2, length - 1))


    mat_x, mat_y = get_matx_maty(voxel_menu_var, uv_scale, mat_num)

    uv_loop = [(mat_x + bufferx, uv_scale*0.66 + mat_y + buffery), (uv_scale + mat_x - bufferx, uv_scale*0.66 + mat_y + buffery), (uv_scale + mat_x - bufferx, uv_scale + mat_y - buffery), (mat_x + bufferx, uv_scale + mat_y - buffery)]
    uvs.append(uv_loop)

        
    
def calculate_smooth_array(smooth_array, vox_array):
     #populate a new array with the average off all the voxel smooth types according to the voxel array number(type)
    vertex_smooth_count = np.zeros((len(vox_array) + 1, len(vox_array[1]) + 1, len(vox_array[1][1]) + 1))
    vertex_smooth_array = np.full((len(vox_array) + 1, len(vox_array[1]) + 1, len(vox_array[1][1]) + 1), -1000.55) #less than -100 considered empty
    for x in range(len(vox_array)):
        for y in range(len(vox_array[x])):
            for z in range(len(vox_array[x][y])):
                if vox_array[x][y][z] > 0:
                    if vox_array[x][y][z] >= len(smooth_array): #vallue can be set to anything even outside array
                        smoothfactor = 0
                    else:
                        smoothfactor = smooth_array[int(vox_array[x][y][z])] 
                    
                    
                    if vertex_smooth_array[x][y][z] < -100:
                        vertex_smooth_array[x][y][z] = smoothfactor
                    else:
                       vertex_smooth_array[x][y][z] = vertex_smooth_array[x][y][z] +  smoothfactor
                    vertex_smooth_count[x][y][z] += 1
                        
                    if vertex_smooth_array[x + 1][y][z] < -100:
                        vertex_smooth_array[x + 1][y][z] =  smoothfactor
                    else:
                        vertex_smooth_array[x + 1][y][z] = vertex_smooth_array[x + 1][y][z] +  smoothfactor
                    vertex_smooth_count[x + 1][y][z] += 1 
                          
                    if vertex_smooth_array[x][y + 1][z] < -100:
                        vertex_smooth_array[x][y + 1][z] =  smoothfactor
                    else:
                        vertex_smooth_array[x][y + 1][z] = vertex_smooth_array[x][y + 1][z] +  smoothfactor 
                    vertex_smooth_count[x][y + 1][z] += 1
                             
                    if vertex_smooth_array[x + 1][y + 1][z] < -100:
                        vertex_smooth_array[x + 1][y + 1][z] =  smoothfactor
                    else:
                        vertex_smooth_array[x + 1][y + 1][z] = vertex_smooth_array[x + 1][y + 1][z] + smoothfactor
                    vertex_smooth_count[x + 1][y + 1][z] += 1
                        
                        
                    if vertex_smooth_array[x][y][z + 1] < -100:
                        vertex_smooth_array[x][y][z + 1] =  smoothfactor
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
                        vertex_smooth_array[x][y + 1][z + 1] = vertex_smooth_array[x][y + 1][z + 1] + smoothfactor
                    vertex_smooth_count[x][y + 1][z + 1] += 1
                    
                    if vertex_smooth_array[x + 1][y + 1][z + 1] < -100:
                        vertex_smooth_array[x + 1][y + 1][z + 1] = smoothfactor
                    else:
                        vertex_smooth_array[x + 1][y + 1][z + 1] = vertex_smooth_array[x + 1][y + 1][z + 1] + smoothfactor
                    vertex_smooth_count[x + 1][y + 1][z + 1] += 1
                    
    for x in range(len(vertex_smooth_array)):
        for y in range(len(vertex_smooth_array[x])):
            for z in range(len(vertex_smooth_array[x][y])):                
                vertex_smooth_array[x][y][z] = vertex_smooth_array[x][y][z]/vertex_smooth_count[x][y][z]
                
    return vertex_smooth_array


def generate_square_voxels(vertex_smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, uv_scale, bufferx, buffery):
    for x in range(len(vox_array)):
        for y in range(len(vox_array[x])):
            for z in range(len(vox_array[x][y])):
                if vox_array[x][y][z] > 0:
                    #add faces x axis
                    if x > 0:
                        if vox_array[x - 1][y][z] == 0:
                            add_xneg_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                    else:
                        add_xneg_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)   
                    if (x + 1) < len(vox_array):
                        if vox_array[x + 1][y][z] == 0:
                            add_xpos_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                    else:
                        add_xpos_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                        
                    #add faces z axis
                    if y > 0:
                        if vox_array[x][y - 1][z] == 0:
                            add_yneg_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                    else:
                        add_yneg_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)   
                    if (y + 1) < len(vox_array[x]):
                        if vox_array[x][y + 1][z] == 0:
                            add_ypos_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                    else:
                        add_ypos_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                        
                    #add faces y axis
                    if z > 0:
                        if vox_array[x][y][z - 1] == 0:
                            add_zneg_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                    else:
                        add_zneg_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery) 
                    if (z + 1) < len(vox_array[x][y]):
                        if vox_array[x][y][z + 1] == 0:
                            add_zpos_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)
                    else:
                        add_zpos_face(vertex_smooth_array, voxel_menu_var, x, y, z, vert_coords, face_vert_indices, uvs, uv_scale, vox_array[x][y][z], bufferx, buffery)