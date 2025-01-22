import bpy
import bmesh
import numpy as np
import mathutils
import math
import  bpy_extras
from bpy_extras import view3d_utils #this library is idiosyncratic
                
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
                    if vertex_smooth_array[x][y][z] < -100:
                        vertex_smooth_array[x][y][z] = smooth_array[int(vox_array[x][y][z])]
                    else:
                       vertex_smooth_array[x][y][z] = vertex_smooth_array[x][y][z] +  smooth_array[int(vox_array[x][y][z])]
                    vertex_smooth_count[x][y][z] += 1
                        
                    if vertex_smooth_array[x + 1][y][z] < -100:
                        vertex_smooth_array[x + 1][y][z] =  smooth_array[int(vox_array[x][y][z])]
                    else:
                        vertex_smooth_array[x + 1][y][z] = vertex_smooth_array[x + 1][y][z] +  smooth_array[int(vox_array[x][y][z])]
                    vertex_smooth_count[x + 1][y][z] += 1 
                          
                    if vertex_smooth_array[x][y + 1][z] < -100:
                        vertex_smooth_array[x][y + 1][z] =  smooth_array[int(vox_array[x][y][z])]
                    else:
                        vertex_smooth_array[x][y + 1][z] = vertex_smooth_array[x][y + 1][z] +  smooth_array[int(vox_array[x][y][z])] 
                    vertex_smooth_count[x][y + 1][z] += 1
                             
                    if vertex_smooth_array[x + 1][y + 1][z] < -100:
                        vertex_smooth_array[x + 1][y + 1][z] =  smooth_array[int(vox_array[x][y][z])]
                    else:
                        vertex_smooth_array[x + 1][y + 1][z] = vertex_smooth_array[x + 1][y + 1][z] +  smooth_array[int(vox_array[x][y][z])]
                    vertex_smooth_count[x + 1][y + 1][z] += 1
                        
                        
                    if vertex_smooth_array[x][y][z + 1] < -100:
                        vertex_smooth_array[x][y][z + 1] =  smooth_array[int(vox_array[x][y][z])]
                    else:
                        vertex_smooth_array[x][y][z + 1] = vertex_smooth_array[x][y][z + 1] +  smooth_array[int(vox_array[x][y][z])]
                    vertex_smooth_count[x][y][z + 1] += 1
                        
                    if vertex_smooth_array[x + 1][y][z + 1] < -100:
                        vertex_smooth_array[x + 1][y][z + 1] =  smooth_array[int(vox_array[x][y][z])]
                    else:
                        vertex_smooth_array[x + 1][y][z + 1] = vertex_smooth_array[x + 1][y][z + 1] +  smooth_array[int(vox_array[x][y][z])] 
                    vertex_smooth_count[x + 1][y][z + 1] += 1
                     
                    if vertex_smooth_array[x][y + 1][z + 1] < -100:
                        vertex_smooth_array[x][y + 1][z + 1] =  smooth_array[int(vox_array[x][y][z])]
                    else:
                        vertex_smooth_array[x][y + 1][z + 1] = vertex_smooth_array[x][y + 1][z + 1] +  smooth_array[int(vox_array[x][y][z])]
                    vertex_smooth_count[x][y + 1][z + 1] += 1
                    
                    if vertex_smooth_array[x + 1][y + 1][z + 1] < -100:
                        vertex_smooth_array[x + 1][y + 1][z + 1] =  smooth_array[int(vox_array[x][y][z])]
                    else:
                        vertex_smooth_array[x + 1][y + 1][z + 1] = vertex_smooth_array[x + 1][y + 1][z + 1] +  smooth_array[int(vox_array[x][y][z])] 
                    vertex_smooth_count[x + 1][y + 1][z + 1] += 1
                    
    for x in range(len(vertex_smooth_array)):
        for y in range(len(vertex_smooth_array[x])):
            for z in range(len(vertex_smooth_array[x][y])):                
                vertex_smooth_array[x][y][z] = vertex_smooth_array[x][y][z]/vertex_smooth_count[x][y][z]
                
    return vertex_smooth_array
      

def generate_mesh_from_array(smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs):
    #prerun to calc all vertex offsets
    uv_scale = 1/voxel_menu_var.voxel_uv_scale
    bufferx = uv_scale*voxel_menu_var.voxel_buffer
    buffery = bufferx/3


   
    vertex_smooth_array = calculate_smooth_array(smooth_array, vox_array)
                     
    print(vertex_smooth_array)
    print(smooth_array[1])
    print(smooth_array[int(vox_array[1][1][1])])
    
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
                        
                    
            
def create_voxel(voxel_menu_var):     
    obj_name = "voxels"

    mesh_data = bpy.data.meshes.new(f"{obj_name}_data")
    mesh_obj = bpy.data.objects.new(obj_name, mesh_data)
    bpy.context.scene.collection.objects.link(mesh_obj)


    mesh_obj.data["voxel_array"] = np.zeros((voxel_menu_var.voxel_dimension_vector[0], 
                                            voxel_menu_var.voxel_dimension_vector[1], 
                                            voxel_menu_var.voxel_dimension_vector[2])).tolist() #numpy doesnt save correctly in blender objects
                                            
    amount_voxel_types = voxel_menu_var.voxel_uv_scale * voxel_menu_var.voxel_uv_scale                       
    mesh_obj.data["voxel_smooth_array"] = np.zeros(amount_voxel_types).tolist()
    
    context = None #its not used just needed for the call
    add_noise(mesh_obj, context, voxel_menu_var)


    

def update_voxel(object, voxel_menu_var): 
    try:
        vox_array = np.array(object.data["voxel_array"])
        
        #array contain smooth settings for voxel types
        amount_voxel_types = voxel_menu_var.voxel_uv_scale * voxel_menu_var.voxel_uv_scale
        voxel_smooth_array = np.array(object.data["voxel_smooth_array"])
        if len(voxel_smooth_array) < amount_voxel_types:
            new_array = np.resize(voxel_smooth_array, (amount_voxel_types))
            print(f"new array: {new_array}") 
            object.data["voxel_smooth_array"] = new_array.tolist()
            voxel_smooth_array = new_array
            
            
        bm = bmesh.new()

        vert_coords = []
        face_vert_indices = []
        
        uvs = []
            
        generate_mesh_from_array(voxel_smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs)
            
        for cord in vert_coords:
            bm.verts.new(cord)
                
        bm.verts.ensure_lookup_table()
            
        for vert_indices in face_vert_indices:
            bm.faces.new([bm.verts[index] for index in vert_indices])
            
        
        uv_layer = bm.loops.layers.uv.verify()
        bm.faces.ensure_lookup_table()
        
        k = 0 #ugly fix in future
        for f in bm.faces:
            i = 0
            for l in f.loops:
                luv = l[uv_layer]
                luv.uv = uvs[k][i]
                i += 1
            k += 1
                
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01) #merge the faces into one mesh
            
        bm.to_mesh(object.data)
        object.data.update()
        bm.free() #free memory used by bm
        
       
       
    except KeyError:
        print(f'{object.name} is not a voxel object, select a voxel object')
        


def add_noise_execute(vox_array, object, context, voxel_menu_var, x, y, z):
    sample_pos = mathutils.Vector((x * voxel_menu_var.noise_scale_vector[0] + voxel_menu_var.noise_offset_vector[0], 
                                    y * voxel_menu_var.noise_scale_vector[1] + voxel_menu_var.noise_offset_vector[1], 
                                    z * voxel_menu_var.noise_scale_vector[2] + voxel_menu_var.noise_offset_vector[2]))
    if mathutils.noise.noise(sample_pos, noise_basis = voxel_menu_var.noise_select_enum) > voxel_menu_var.noise_cutoff:
        if vox_array[x][y][z] == voxel_menu_var.voxel_number1:
            vox_array[x][y][z] = voxel_menu_var.voxel_number

    
def fill_voxel_execute(vox_array, object, context, voxel_menu_var, x, y, z): 
    vox_array[x][y][z] = voxel_menu_var.voxel_number


def replace_content_execute(vox_array, object, context, voxel_menu_var, x, y, z):
    if vox_array[x][y][z] == voxel_menu_var.voxel_number:
        vox_array[x][y][z] = voxel_menu_var.voxel_number1      

#for grass covering surfaces etc
def rayscan_replace_content_execute(vox_array, object, context, voxel_menu_var, x, y, z):
    if vox_array[x][y][z] == voxel_menu_var.voxel_number:
        vox_pos_x = x + voxel_menu_var.voxel_rayscan_dir[0]  
        vox_pos_y = y + voxel_menu_var.voxel_rayscan_dir[1] 
        vox_pos_z = z + voxel_menu_var.voxel_rayscan_dir[2]
          
        if ((vox_pos_x >= 0) and (vox_pos_x < len(vox_array))): #if voxel next diffrent change
            if ((vox_pos_y >= 0) and (vox_pos_y < len(vox_array[1]))):
                if ((vox_pos_z >= 0) and (vox_pos_z < len(vox_array[1][1]))): 
                    #or stops changing all numbers if start from negative position      
                    if vox_array[vox_pos_x][vox_pos_y][vox_pos_z] != voxel_menu_var.voxel_number and vox_array[vox_pos_x][vox_pos_y][vox_pos_z] != voxel_menu_var.voxel_number1:
                        vox_array[x][y][z] = voxel_menu_var.voxel_number1
                else:
                    vox_array[x][y][z] = voxel_menu_var.voxel_number1 #if voxel next is outside voxels change
            else:
                vox_array[x][y][z] = voxel_menu_var.voxel_number1
        else:
            vox_array[x][y][z] = voxel_menu_var.voxel_number1


def voxify_execute(vox_array, object, context, voxel_menu_var, x, y, z):
    ray_dir = mathutils.Vector((0, 0, 1)) #straight up
    hit, loc, norm, idx, obj, mw = context.scene.ray_cast(context.view_layer.depsgraph, (x, y, z), ray_dir)
    if hit:
        if norm.dot(ray_dir) > 0:
            vox_array[x][y][z] = voxel_menu_var.voxel_number


def try_for_all_voxels(object, context, voxel_menu_var, function_to_execute):
    try:
        vox_array = np.array(object.data["voxel_array"])
        object.hide_viewport = True #suppose to stop self trigger
        for x in range(len(vox_array)):
            for y in range(len(vox_array[x])):
                for z in range(len(vox_array[x][y])):
                    function_to_execute(vox_array, object, context, voxel_menu_var, x, y, z)

                        
        object.data["voxel_array"] = vox_array.tolist() 
        object.hide_viewport = False
    except KeyError:
        print(f'{object.name} is not a voxel object, select a voxel object')
        return
    update_voxel(object, voxel_menu_var)


#trace up in scene if hit back face inside else not
def voxify(object, context, voxel_menu_var):
    function_to_execute = voxify_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)


def fill_voxel(object, context, voxel_menu_var):
    function_to_execute = fill_voxel_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)

def rayscan_replace_content(object, context, voxel_menu_var):
    function_to_execute = rayscan_replace_content_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)

def replace_content(object, context, voxel_menu_var):
    function_to_execute = replace_content_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)


def add_noise(object, context, voxel_menu_var):
    function_to_execute = add_noise_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)



#Tools

def change_cell_value(object, x, y, z, vox_array, voxel_menu_var, val):
    vox_array[x][y][z] = val
    object.data["voxel_array"] = vox_array.tolist() 


def probe_cell_value(object, x, y, z, vox_array,  voxel_menu_var, val):
    voxel_menu_var.voxel_number_prob = int(vox_array[x][y][z])
    for area in bpy.context.screen.areas:
        area.tag_redraw()


#set the voxel smooth aray index cell clicked to the smooth amount selected in the menu
def probe_set_voxel_smoothness(object, x, y, z, vox_array, voxel_menu_var, val):
    voxel_smooth_array = np.array(object.data["voxel_smooth_array"])
    voxel_smooth_array[int(vox_array[x][y][z])] = voxel_menu_var.voxel_smooth_amount
    object.data["voxel_smooth_array"] = voxel_smooth_array.tolist()
    print(voxel_smooth_array)


        
def execute_at_position(object, offset_position,  voxel_menu_var, val, function_to_execute):
    try:
        vox_array = np.array(object.data["voxel_array"])
        x = math.floor(offset_position.x)
        y = math.floor(offset_position.y)
        z = math.floor(offset_position.z)
        if ((x >= 0) and (x < len(vox_array))):
            if ((y >= 0) and (y < len(vox_array[1]))):
                if ((z >= 0) and (z < len(vox_array[1][1]))):
                    function_to_execute(object, x, y, z, vox_array, voxel_menu_var, val)
                    
    except KeyError:
        print(f'{object.name} is not a voxel object, select a voxel object')
        return
    update_voxel(object, voxel_menu_var)       
        
        
def execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute):
    coord = mouse_x, mouse_y
    #cast ray from mouse location and return data from ray
    region = context.region
    rv3d = context.region_data
    #get ray from viewport and mouse
    view_vector = bpy_extras.view3d_utils.region_2d_to_vector_3d(region, rv3d, coord) #this is direction
    ray_origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(region, rv3d, coord) #this is start

    hit, location, normal, index, object, matrix = context.scene.ray_cast(context.view_layer.depsgraph, ray_origin, view_vector)
    if hit:
        if add == True:
            offset_position = location - ((ray_origin - location).normalized() * voxel_menu_var.voxel_tool_add)
            val = voxel_menu_var.voxel_number
        else:
            offset_position = location - ((ray_origin - location).normalized() * voxel_menu_var.voxel_tool_edit)
            val = voxel_menu_var.voxel_number1
            
        offset_position_obj_space = object.matrix_world.inverted() @ offset_position #get position in obj space
        execute_at_position(object, offset_position_obj_space, voxel_menu_var, val, function_to_execute)
        

def tool_probe_set_voxel_smoothness(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    function_to_execute = probe_set_voxel_smoothness
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute)
    
    
def tool_probe_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    function_to_execute = probe_cell_value
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute)
    
    
def tool_trace_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    function_to_execute = change_cell_value
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute)
    