import bpy
import bmesh
import numpy as np
import mathutils
import math
import  bpy_extras
from bpy_extras import view3d_utils #this library is idiosyncratic

import sys
import os
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import VoxelInstance
import VoxelMarchingCubes
import VoxelsCubes
import Voxel_triangle_square
import Voxels_traingle_hex
import imp
imp.reload(VoxelMarchingCubes)
imp.reload(VoxelsCubes)
imp.reload(Voxel_triangle_square)
imp.reload(Voxels_traingle_hex)
imp.reload(VoxelInstance)
import re


def remove_children(voxel_object):
    for child in voxel_object.children:
        try:
            bpy.context.scene.collection.objects.unlink(child)
        except:
            pass

def get_matx_maty(voxel_menu_var, uv_scale, mat_num):
    num = mat_num - 1
    mat_x = (num % voxel_menu_var.voxel_uv_scale)*uv_scale #x offset
    mat_y = (math.floor(num / voxel_menu_var.voxel_uv_scale))*uv_scale #yoffset
    return (mat_x, mat_y)

def generate_mesh_from_array(smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, object):

    #prerun to calc all vertex offsets
    uv_scale = 1/voxel_menu_var.voxel_uv_scale
    uv_scale3 = uv_scale/3
    bufferx = uv_scale*voxel_menu_var.voxel_buffer
    buffery = bufferx/3

    #if change from object instance need get rid those
    remove_children(object)

    if voxel_menu_var.voxel_type_select_enum == 'CUBES':
       vertex_smooth_array = VoxelsCubes.calculate_smooth_array(smooth_array, vox_array)
       print(vertex_smooth_array)
       print(vertex_smooth_array.shape)
       VoxelsCubes.generate_square_voxels(vertex_smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, uv_scale, bufferx, buffery)                
    elif voxel_menu_var.voxel_type_select_enum == 'MARCHING_CUBES':
       VoxelMarchingCubes.generate_marching_cubes_voxels(smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, uv_scale, uv_scale3)
    elif voxel_menu_var.voxel_type_select_enum == 'OBJECT_INSTANCES':
        VoxelInstance.make_object_voxel(vox_array, object)
    elif voxel_menu_var.voxel_type_select_enum ==   'HEX_PRISM':
        vertex_smooth_array = Voxels_traingle_hex.calculate_hex_smooth_array(smooth_array, vox_array)
        Voxels_traingle_hex.generate_hex_prism_voxels(vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, uv_scale, bufferx, buffery, vertex_smooth_array)
    elif voxel_menu_var.voxel_type_select_enum ==   'SQUARE_PRISM':
        vertex_smooth_array = Voxel_triangle_square.calculate_square_smooth_array(smooth_array, vox_array)
        Voxel_triangle_square.generate_square_prism_voxels(vertex_smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, uv_scale, bufferx, buffery)
    
         
            
def create_voxel(voxel_menu_var):     
    obj_name = "voxels"

    mesh_data = bpy.data.meshes.new(f"{obj_name}_data")
    mesh_obj = bpy.data.objects.new(obj_name, mesh_data)
    bpy.context.scene.collection.objects.link(mesh_obj)


    mesh_obj.data["voxel_array"] = np.zeros((voxel_menu_var.voxel_dimension_vector[0], 
                                            voxel_menu_var.voxel_dimension_vector[1], 
                                            voxel_menu_var.voxel_dimension_vector[2])).tolist() #numpy doesnt save correctly in blender objects
                                            
    amount_voxel_types = voxel_menu_var.voxel_uv_scale * voxel_menu_var.voxel_uv_scale                       
    mesh_obj.data["voxel_smooth_array"] = np.zeros(amount_voxel_types + 1).tolist()
    
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
            
        generate_mesh_from_array(voxel_smooth_array, vox_array, vert_coords, face_vert_indices, voxel_menu_var, uvs, object)
            
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
    gradient_val_x = (voxel_menu_var.noise_gradient_max[0] - voxel_menu_var.noise_gradient_min[0]) / len(vox_array) * x + voxel_menu_var.noise_gradient_min[0]
    gradient_val_y = (voxel_menu_var.noise_gradient_max[1] - voxel_menu_var.noise_gradient_min[1]) / len(vox_array[1]) * y + voxel_menu_var.noise_gradient_min[1]
    gradient_val_z = (voxel_menu_var.noise_gradient_max[2] - voxel_menu_var.noise_gradient_min[2]) / len(vox_array[1][1]) * z + voxel_menu_var.noise_gradient_min[2]
    
    gradient_val = gradient_val_x + gradient_val_y + gradient_val_z

    
    sample_pos = mathutils.Vector((x * voxel_menu_var.noise_scale_vector[0] + voxel_menu_var.noise_offset_vector[0], 
                                    y * voxel_menu_var.noise_scale_vector[1] + voxel_menu_var.noise_offset_vector[1], 
                                    z * voxel_menu_var.noise_scale_vector[2] + voxel_menu_var.noise_offset_vector[2]))
    if mathutils.noise.noise(sample_pos, noise_basis = voxel_menu_var.noise_select_enum) + gradient_val > voxel_menu_var.noise_cutoff:
        if vox_array[x][y][z] == voxel_menu_var.voxel_number1:
            vox_array[x][y][z] = voxel_menu_var.voxel_number

    
def fill_voxel_execute(vox_array, object, context, voxel_menu_var, x, y, z): 
    vox_array[x][y][z] = voxel_menu_var.voxel_number
    
def clear_voxel_execute(vox_array, object, context, voxel_menu_var, x, y, z): 
    vox_array[x][y][z] = 0


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


#foot tool function
def comparepoints(pointtop, pointbottom, vox_array):
    #top valid
    if pointtop[0] > 0 and pointtop[0] < len(vox_array) - 1: #x
        if pointtop[1] > 0 and pointtop[1] < len(vox_array[0]) - 1: #y
            if pointtop[2] > 0 and pointtop[2] < len(vox_array[0][0]) - 1: #y
                #bottom valid
                if pointbottom[0] > 0 and pointbottom[0] < len(vox_array) - 1: #x
                    if pointbottom[1] > 0 and pointbottom[1] < len(vox_array[0]) - 1: #y
                        if pointbottom[2] > 0 and pointbottom[2] < len(vox_array[0][0]) - 1: #y
                            #check
                            if vox_array[pointtop[0]][pointtop[1]][pointtop[2]] == 0:
                                if vox_array[pointbottom[0]][pointbottom[1]][pointbottom[2]] != 0:
                                    return True
    return False
 
                                    
def check_positions(currentpos, checkpos, vox_array, voxel_menu_var):
#get all points perpendicular
    top_points = []
    bottom_points = []
    if currentpos[0] == checkpos[0]: #x
        top_points.append((currentpos[0] + 1, currentpos[1], currentpos[2]))
        top_points.append((currentpos[0] - 1, currentpos[1], currentpos[2]))
        
        bottom_points.append((checkpos[0] + 1, checkpos[1], checkpos[2]))
        bottom_points.append((checkpos[0] - 1, checkpos[1], checkpos[2]))
    if currentpos[1] == checkpos[1]: #y
        top_points.append((currentpos[0], currentpos[1] + 1, currentpos[2]))
        top_points.append((currentpos[0], currentpos[1] - 1, currentpos[2]))
        
        bottom_points.append((checkpos[0], checkpos[1] + 1, checkpos[2]))
        bottom_points.append((checkpos[0], checkpos[1] - 1, checkpos[2]))
    if currentpos[2] == checkpos[2]: #z
        top_points.append((currentpos[0], currentpos[1], currentpos[2] + 1))
        top_points.append((currentpos[0], currentpos[1], currentpos[2] - 1))
        
        bottom_points.append((checkpos[0], checkpos[1], checkpos[2] + 1))
        bottom_points.append((checkpos[0], checkpos[1], checkpos[2] - 1))
       
    for i in range(len(top_points)): 
        if comparepoints(top_points[i], bottom_points[i], vox_array) == True:
            vox_array[currentpos[0]][currentpos[1]][currentpos[2]] = voxel_menu_var.voxel_number1
            return  

#for grass at base of cliffs etc
def foot_replace_content_execute(vox_array, object, context, voxel_menu_var, x, y, z):
    #this doesnt make sense for arbitrary axis, first axis not 0 is assumed direction
    #get point next to point in that direction
    if vox_array[x][y][z] == voxel_menu_var.voxel_number:
        if voxel_menu_var.voxel_rayscan_dir[0] != 0: #x
            check_positions((x, y, z), (x - voxel_menu_var.voxel_rayscan_dir[0], y, z), vox_array, voxel_menu_var)
        elif voxel_menu_var.voxel_rayscan_dir[1] != 0: #y+
            check_positions((x, y, z), (x, y - voxel_menu_var.voxel_rayscan_dir[1], z), vox_array, voxel_menu_var)
        elif voxel_menu_var.voxel_rayscan_dir[2] != 0: #z+
            check_positions((x, y, z), (x, y, z - voxel_menu_var.voxel_rayscan_dir[2]), vox_array, voxel_menu_var)
 
    
    '''if vox_array[x][y][z] == voxel_menu_var.voxel_number:
        perp to that
        
        if z > 0:   
            if x > 0:
                if vox_array[x - 1][y][z] == 0:
                    if vox_array[x - 1][y][z - 1] != 0:
                        vox_array[x][y][z] = voxel_menu_var.voxel_number1
            if x < len(vox_array) - 1:
                if vox_array[x + 1][y][z] == 0:
                    if vox_array[x + 1][y][z - 1] != 0:
                        vox_array[x][y][z] = voxel_menu_var.voxel_number1
            if y > 0:
                if vox_array[x][y - 1][z] == 0:
                    if vox_array[x][y - 1][z - 1] != 0:
                        vox_array[x][y][z] = voxel_menu_var.voxel_number1
            if y < len(vox_array[x]) - 1:
                if vox_array[x][y + 1][z] == 0:
                    if vox_array[x][y + 1][z - 1] != 0:
                        vox_array[x][y][z] = voxel_menu_var.voxel_number1'''
                

def voxify_execute(vox_array, object, context, voxel_menu_var, x, y, z):
    ray_dir = mathutils.Vector((0, 0, 1)) #straight up
    hit, loc, norm, idx, obj, mw = context.scene.ray_cast(context.view_layer.depsgraph, (x, y, z), ray_dir)
    if hit:
        if norm.dot(ray_dir) > 0:
            vox_array[x][y][z] = voxel_menu_var.voxel_number


def try_for_all_voxels(object, context, voxel_menu_var, function_to_execute):
    try:
        vox_array = np.array(object.data["voxel_array"])
        print(vox_array.shape)
        object.hide_viewport = True #suppose to stop self trigger
        for x in range(len(vox_array)):
            for y in range(len(vox_array[x])):
                for z in range(len(vox_array[x][y])):
                    function_to_execute(vox_array, object, context, voxel_menu_var, x, y, z)

        print(vox_array.shape)              
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
   
def foot_replace_content(object, context, voxel_menu_var):
    function_to_execute = foot_replace_content_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute) 

def replace_content(object, context, voxel_menu_var):
    function_to_execute = replace_content_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)


def add_noise(object, context, voxel_menu_var):
    function_to_execute = add_noise_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)

def clear_voxel(object, context, voxel_menu_var):
    function_to_execute = clear_voxel_execute
    try_for_all_voxels(object, context, voxel_menu_var, function_to_execute)

#Tools

def change_cell_value(object, x, y, z, vox_array, voxel_menu_var, val, add, context):
    vox_array[x][y][z] = val
    object.data["voxel_array"] = vox_array.tolist() 

def paint_cell_values(object, x, y, z, vox_array, voxel_menu_var, val, add, context):
    for x_axis in range(len(vox_array)):
        for y_axis in range(len(vox_array[0])):
            for z_axis in range(len(vox_array[0][0])):
                #faster to calc squares than square roots
                distance_squared = (x - x_axis)**2 + (y - y_axis)**2 + (z - z_axis)**2
                if distance_squared < voxel_menu_var.voxel_brushwidth**2:
                    if add == True: #add
                        vox_array[x_axis][y_axis][z_axis] = val
                    else: #edit 1 with 2
                        if vox_array[x_axis][y_axis][z_axis] == voxel_menu_var.voxel_number:
                            vox_array[x_axis][y_axis][z_axis] = voxel_menu_var.voxel_number1
                        
    object.data["voxel_array"] = vox_array.tolist() 

def paint_surface_values(object, x, y, z, vox_array, voxel_menu_var, val, add, context):
    for x_axis in range(len(vox_array)):
        for y_axis in range(len(vox_array[0])):
            for z_axis in range(len(vox_array[0][0])):
                #faster to calc squares than square roots
                distance_squared = (x - x_axis)**2 + (y - y_axis)**2 + (z - z_axis)**2
                if distance_squared < voxel_menu_var.voxel_brushwidth**2:
                    #direction = mathutils.Vector((0, 0, -1))
                    direction = mathutils.Vector(voxel_menu_var.voxel_rayscan_dir).normalized()
                    world_space_coords = object.matrix_world @ mathutils.Vector((x_axis, y_axis, z_axis))
                    hit, location, normal, index, object_hit, matrix = context.scene.ray_cast(context.view_layer.depsgraph, world_space_coords, direction)
                    if hit:
                        distance_squared = (world_space_coords.x - location.x)**2 + (world_space_coords.y - location.y)**2 + (world_space_coords.z - location.z)**2
                        if distance_squared < voxel_menu_var.voxel_tool_surface_dist**2:
                            if add == True: #add
                                if vox_array[x_axis][y_axis][z_axis] == 0:
                                    vox_array[x_axis][y_axis][z_axis] = voxel_menu_var.voxel_number
                            else:
                                if vox_array[x_axis][y_axis][z_axis] != 0:
                                    vox_array[x_axis][y_axis][z_axis] = voxel_menu_var.voxel_number
                        
    object.data["voxel_array"] = vox_array.tolist() 


def probe_cell_value(object, x, y, z, vox_array,  voxel_menu_var, val, add, context):
    voxel_menu_var.voxel_number_prob = int(vox_array[x][y][z])
    for area in bpy.context.screen.areas:
        area.tag_redraw()


#set the voxel smooth aray index cell clicked to the smooth amount selected in the menu
def probe_set_voxel_smoothness(object, x, y, z, vox_array, voxel_menu_var, val, add, context):
    voxel_smooth_array = np.array(object.data["voxel_smooth_array"])
     
    if int(vox_array[x][y][z]) < len(voxel_smooth_array):         
        voxel_smooth_array[int(vox_array[x][y][z])] = voxel_menu_var.voxel_smooth_amount
    else:
        print('voxel number out uv texture bounds')
    voxel_smooth_array[0] = 0 #this is something else can mess up smoothness
    object.data["voxel_smooth_array"] = voxel_smooth_array.tolist()


       
def execute_at_position(object, offset_position,  voxel_menu_var, val, function_to_execute, add, skip_inside_check, context):
    try:
        vox_array = np.array(object.data["voxel_array"])
        x = math.floor(offset_position.x)
        y = math.floor(offset_position.y)
        z = math.floor(offset_position.z)
        if skip_inside_check == True:
            function_to_execute(object, x, y, z, vox_array, voxel_menu_var, val, add, context)
        else:
            if ((x >= 0) and (x < len(vox_array))):
                if ((y >= 0) and (y < len(vox_array[1]))):
                    if ((z >= 0) and (z < len(vox_array[1][1]))):
                        function_to_execute(object, x, y, z, vox_array, voxel_menu_var, val, add, context)
                    
    except KeyError:
        print(f'{object.name} is not a voxel object, select a voxel object')
        return
    update_voxel(object, voxel_menu_var)       
        
        
def execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute, skip_inside_check):
    coord = mouse_x, mouse_y
    #cast ray from mouse location and return data from ray
    region = context.region
    rv3d = context.region_data
    #get ray from viewport and mouse
    view_vector = bpy_extras.view3d_utils.region_2d_to_vector_3d(region, rv3d, coord) #this is direction
    ray_origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(region, rv3d, coord) #this is start

    hit, location, normal, index, object_hit, matrix = context.scene.ray_cast(context.view_layer.depsgraph, ray_origin, view_vector)
    
    if hit:
        if add == True:
            offset_position = location - ((ray_origin - location).normalized() * voxel_menu_var.voxel_tool_add)
            val = voxel_menu_var.voxel_number
        else:
            offset_position = location - ((ray_origin - location).normalized() * voxel_menu_var.voxel_tool_edit)
            val = voxel_menu_var.voxel_number1
            
        offset_position_obj_space = object.matrix_world.inverted() @ offset_position #get position in obj space
        execute_at_position(object, offset_position_obj_space, voxel_menu_var, val, function_to_execute, add, skip_inside_check, context)
        


def tool_probe_set_voxel_smoothness(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    function_to_execute = probe_set_voxel_smoothness
    skip_inside_check = False
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute, skip_inside_check)
    
    
def tool_probe_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    function_to_execute = probe_cell_value
    skip_inside_check = False
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute, skip_inside_check)
    
    
def tool_trace_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    function_to_execute = change_cell_value
    skip_inside_check = False
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute, skip_inside_check)
    
    
def tool_paint_cell_values(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    skip_inside_check = True
    function_to_execute = paint_cell_values
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute, skip_inside_check)
    
def tool_paint_surface_values(mouse_x, mouse_y, object, context, add, voxel_menu_var):
    skip_inside_check = True
    function_to_execute = paint_surface_values
    execute_function_on_clicked_voxel(mouse_x, mouse_y, object, context, add, voxel_menu_var, function_to_execute, skip_inside_check)