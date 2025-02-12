bl_info = {
    "name" : "Voxels for Blender",
    "authur" : "keskisan",
    "version" : (1, 0),
    "blender" : (4,3,2),
    "location" : "View3d > UI",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Add Mesh",
}

import bpy
import sys
import os

from bpy.props import IntProperty, IntVectorProperty, FloatVectorProperty, FloatProperty, BoolProperty, EnumProperty


#my files
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    

import Voxels
import imp
imp.reload(Voxels)


#custom properties to main panel
class VoxelProperties(bpy.types.PropertyGroup):
    voxel_dimension_vector : IntVectorProperty(name="Dimensions", default=(3, 3, 3), min=1)
    noise_scale_vector:  FloatVectorProperty(name="Noise Scale")
    noise_offset_vector:  FloatVectorProperty(name="Noise Offset")
    noise_gradient_min:  FloatVectorProperty(name="Noise Gradient Min")
    noise_gradient_max:  FloatVectorProperty(name="Noise Gradient Max")
    noise_cutoff: FloatProperty(name="Noise CutOff", default=0.33)
    voxel_smooth_amount: FloatProperty(name="Voxel_Smooth Amount")
    voxel_tool_add: FloatProperty(name="tool add", default=-0.4)
    voxel_tool_edit: FloatProperty(name="tool edit", default=0.4)
    voxel_tool_surface_dist: FloatProperty(name="scan dist", default=0.5)
    voxel_number: IntProperty(name="number to use 1", default=1, min=0)
    voxel_number1: IntProperty(name="number to use 2", default=1, min=0)
    voxel_number_prob: IntProperty(name="number probed")
    voxel_uv_scale: IntProperty(name="uv scale", default=2, min=1)
    voxel_buffer: FloatProperty(name="uv buffer", default=0, min=0, max=1)
    voxel_rayscan_dir: IntVectorProperty(name="direction", min=-1, max=1)
    voxel_topCover: FloatProperty(name="top cover",default = -0.5, min=-1, max=0)
    voxel_bottomCover: FloatProperty(name="bottom cover",default = 0.8, min=0, max=1)
    voxel_brushwidth: FloatProperty(name="brushwidth",default = 1, min=0)

    subpanel_noise_status: BoolProperty(name="Show noise options", default=False)
    subpanel_add_voxel: BoolProperty(name="Show add voxel", default=False)
    subpanel_voxel_settings: BoolProperty(name="Show voxel options", default=False)
    subpanel_obj_to_voxel: BoolProperty(name="object to voxel", default=False)
    subpanel_voxel_tool: BoolProperty(name="tool for editing voxel", default=False)
    subpanel_uvs: BoolProperty(name="uv settings", default=False)
    
    noise_select_enum : EnumProperty(
        name= "Noise",
        description="Noise type to be used",
        items=[('BLENDER', "Blender", ""),
                ('PERLIN_ORIGINAL', "Perlin_original", ""),
                ('PERLIN_NEW', "Perlin_new", ""),
                ('VORONOI_F1', "Voronoi_F1", ""),
                ('VORONOI_F2', "Voronoi_F2", ""),
                ('VORONOI_F3', "Voronoi_F3", ""),
                ('VORONOI_F4', "Voronoi_F4", ""),
                ('VORONOI_F2F1', "Voronoi_F2F1", ""),
                ('VORONOI_CRACKLE', "Voronoi_crackle", ""),
                ('CELLNOISE', "Cellnoise", "")
        ]
    )
    
    voxel_type_select_enum : EnumProperty(
        name= "Type",
        description="Voxel type to be used",
        items=[('CUBES', "Cubes", ""),
                ('MARCHING_CUBES', "marching_cubes", ""),
                ('OBJECT_INSTANCES', "object_instances", ""),
                ('HEX_PRISM', "hex_prism", ""),
                ('SQUARE_PRISM', "square_prism", "")       
        ]
    )


class VOXEL_PT_main_panel(bpy.types.Panel):
    """Creates a Voxel Panel in the Object properties window"""
    bl_label = "Add voxel Panel"
    bl_idname = "VOXEL_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "voxel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var

        layout.operator("voxel.update_voxel")
        layout.label(text='numbers used for voxels, 0 clear')
        layout.prop(voxel_menu_var, "voxel_number")
        layout.prop(voxel_menu_var, "voxel_number1")
        layout.label(text='direction 0 0 1 is up')
        layout.prop(voxel_menu_var, "voxel_rayscan_dir")
        
        layout.operator(ModalOperator_voxel_probe.bl_idname, text=ModalOperator_voxel_probe.bl_label)
        layout.label(text=f'number probed: {voxel_menu_var.voxel_number_prob}')
        
        layout.prop(voxel_menu_var, "subpanel_add_voxel") #Add voxel
        if voxel_menu_var.subpanel_add_voxel:
            box1 = layout.box()
            box1.label(text='set dims click add and select obj to edit')
            box1.operator("voxel.add_voxel")
            box1.prop(voxel_menu_var, "voxel_dimension_vector")
        
        layout.prop(voxel_menu_var, "subpanel_voxel_settings") #voxel options
        if voxel_menu_var.subpanel_voxel_settings:
            box2 = layout.box()
            box2.label(text='voxel type')
            box2.prop(voxel_menu_var, "voxel_type_select_enum")
            box2.label(text='smooth tool set voxel type to smooth amount')
            box2.prop(voxel_menu_var, "voxel_smooth_amount")
            box2.operator(ModalOperator_voxel_set_smoothness.bl_idname, text=ModalOperator_voxel_set_smoothness.bl_label)
            box2.label(text='fill voxel with number to use')
            box2.operator("voxel.fill_voxel")
            box2.operator("voxel.clear_voxel")
            box2.operator("voxel.replace_content")
            box2.label(text='uses direction')
            box2.operator("voxel.rayscan_replace_content")
            box2.label(text='uses direction')
            box2.operator("voxel.foot_replace_content")
        
        layout.prop(voxel_menu_var, "subpanel_obj_to_voxel") #object to voxel
        if voxel_menu_var.subpanel_obj_to_voxel:
            box3 = layout.box()
            box3.label(text='place voxels at intersecting meshes')
            box3.operator("voxel.voxify")
        
        layout.prop(voxel_menu_var, "subpanel_voxel_tool") #edit tool
        if voxel_menu_var.subpanel_voxel_tool:
            box4 = layout.box()
            box4.label(text='Q add, W edit, right click or esc done')
            box4.label(text='can place on intersecting meshes')
            box4.operator(ModalOperator_voxel_tool.bl_idname, text=ModalOperator_voxel_tool.bl_label)
            box4.label(text='Q fill with 1, W replaces 1 with 2')
            box4.operator(ModalOperator_voxel_paint_tool.bl_idname, text=ModalOperator_voxel_paint_tool.bl_label)
            box4.label(text='adjust position of edit, add if needed')
            box4.prop(voxel_menu_var, "voxel_tool_add")
            box4.prop(voxel_menu_var, "voxel_tool_edit")
            box4.prop(voxel_menu_var, "voxel_brushwidth")
            box4.label(text='uses direction')
            box4.operator(ModalOperator_voxel_paint_surface_tool.bl_idname, text=ModalOperator_voxel_paint_surface_tool.bl_label)
            box4.prop(voxel_menu_var, "voxel_tool_surface_dist")
            

        layout.prop(voxel_menu_var, "subpanel_noise_status") #noise
        if voxel_menu_var.subpanel_noise_status:
            box = layout.box()
            box.operator("voxel.add_noise")
            box.prop(voxel_menu_var, "noise_scale_vector")
            box.prop(voxel_menu_var, "noise_offset_vector")
            box.label(text='bias noise -empty +full')
            box.prop(voxel_menu_var, "noise_gradient_min")
            box.prop(voxel_menu_var, "noise_gradient_max")
            box.prop(voxel_menu_var, "noise_cutoff")
            box.prop(voxel_menu_var, "noise_select_enum")

        layout.prop(voxel_menu_var, "subpanel_uvs") #uvs
        if voxel_menu_var.subpanel_noise_status:
            box5 = layout.box()
            box5.prop(voxel_menu_var, "voxel_uv_scale")
            box5.prop(voxel_menu_var, "voxel_buffer")
            box5.label(text='cubematching texture cover')
            box5.prop(voxel_menu_var, "voxel_topCover")
            box5.prop(voxel_menu_var, "voxel_bottomCover")
            



class VOXEL_OT_add_voxel(bpy.types.Operator):
    bl_label = "Add Voxel"
    bl_idname = "voxel.add_voxel"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var

        Voxels.create_voxel(voxel_menu_var)
        return {'FINISHED'}
   
    
class VOXEL_OT_update_voxel(bpy.types.Operator):
    bl_label = "Update Voxel"
    bl_idname = "voxel.update_voxel"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.update_voxel(bpy.context.object, voxel_menu_var)

        return {'FINISHED'}    
    
    
       
    
class VOXEL_OT_fill_voxel(bpy.types.Operator):
    bl_label = "Fill Voxel (1)"
    bl_idname = "voxel.fill_voxel"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.fill_voxel(bpy.context.object, context, voxel_menu_var)

        return {'FINISHED'}
    

class VOXEL_OT_clear_voxel(bpy.types.Operator):
    bl_label = "Clear Voxel"
    bl_idname = "voxel.clear_voxel"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.clear_voxel(bpy.context.object, context, voxel_menu_var)

        return {'FINISHED'}
     
    
    
class VOXEL_OT_replace_content(bpy.types.Operator):
    bl_label = "Replace (1 with 2)"
    bl_idname = "voxel.replace_content"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.replace_content(bpy.context.object, context, voxel_menu_var)

        return {'FINISHED'}
    
    
class VOXEL_OT_rayscan_replace_content(bpy.types.Operator):
    bl_label = "rayscan replace (1 with 2)"
    bl_idname = "voxel.rayscan_replace_content"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.rayscan_replace_content(bpy.context.object, context, voxel_menu_var)

        return {'FINISHED'}

class VOXEL_OT_foot_replace_content(bpy.types.Operator):
    bl_label = "foot replace (1 with 2)"
    bl_idname = "voxel.foot_replace_content"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.foot_replace_content(bpy.context.object, context, voxel_menu_var)

        return {'FINISHED'}

class VOXEL_OT_add_noise(bpy.types.Operator):
    bl_label = "Add noise (fill 2 with 1)"
    bl_idname = "voxel.add_noise"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.add_noise(bpy.context.object, context, voxel_menu_var)
        return {'FINISHED'}


class VOXEL_OT_voxify(bpy.types.Operator):
    bl_label = "Make Object Voxel (1)"
    bl_idname = "voxel.voxify"
    
    def execute(self, context):
        scene = context.scene
        voxel_menu_var = scene.voxel_menu_var
        
        Voxels.voxify(bpy.context.object, context, voxel_menu_var)
        return {'FINISHED'}
    



class ModalOperator_voxel_tool(bpy.types.Operator):
    """Add and edit voxel tool"""
    bl_idname = "object.modal_operator_add_edit"
    bl_label = "Voxel tool (Q=1 W=2)"

    mouse_x: IntProperty()
    mouse_y: IntProperty()

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            self.mouse_x = event.mouse_region_x
            self.mouse_y = event.mouse_region_y
        
        if (event.type == 'Q') and (event.value == 'RELEASE'): #add
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = True
            Voxels.tool_trace_voxel(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)

        if (event.type == 'W') and (event.value == 'RELEASE'): #edit
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = False
            Voxels.tool_trace_voxel(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)
            
       
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'FINISHED'}

        return {'RUNNING_MODAL'} 
        #return {'PASS_THROUGH'} #taken bindings seem to mess with it
    
    def invoke(self, context, event):
        if context.object:
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


class ModalOperator_voxel_paint_tool(bpy.types.Operator):
    """bruch add and edit voxel tool"""
    bl_idname = "object.modal_operator_paint_add_edit"
    bl_label = "Voxel paint tool (Q=1 W=2)"

    mouse_x: IntProperty()
    mouse_y: IntProperty()

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            self.mouse_x = event.mouse_region_x
            self.mouse_y = event.mouse_region_y
        
        if (event.type == 'Q') and (event.value == 'RELEASE'): #add
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = True
            print( bpy.context.object.name)
            Voxels.tool_paint_cell_values(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)

        if (event.type == 'W') and (event.value == 'RELEASE'): #edit
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = False
            print( bpy.context.object.name)
            Voxels.tool_paint_cell_values(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)
            
       
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'FINISHED'}

        return {'RUNNING_MODAL'} 
        #return {'PASS_THROUGH'} #taken bindings seem to mess with it
    
    def invoke(self, context, event):
        if context.object:
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}

class ModalOperator_voxel_paint_surface_tool(bpy.types.Operator):
    """bruch add and edit voxel tool"""
    bl_idname = "object.modal_operator_paint_surface"
    bl_label = "Voxel paint surface tool (Q=1 W=2)"

    mouse_x: IntProperty()
    mouse_y: IntProperty()

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            self.mouse_x = event.mouse_region_x
            self.mouse_y = event.mouse_region_y
        
        if (event.type == 'Q') and (event.value == 'RELEASE'): #add
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = True
            print( bpy.context.object.name)
            Voxels.tool_paint_surface_values(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)

        if (event.type == 'W') and (event.value == 'RELEASE'): #edit
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = False
            print( bpy.context.object.name)
            Voxels.tool_paint_surface_values(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)
            
       
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'FINISHED'}

        return {'RUNNING_MODAL'} 
        #return {'PASS_THROUGH'} #taken bindings seem to mess with it
    
    def invoke(self, context, event):
        if context.object:
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


class ModalOperator_voxel_probe(bpy.types.Operator):
    """get voxel number tool"""
    bl_idname = "object.modal_operator_probe"
    bl_label = "Probe voxel number"

    mouse_x: IntProperty()
    mouse_y: IntProperty()

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            self.mouse_x = event.mouse_region_x
            self.mouse_y = event.mouse_region_y
        
        if (event.type == 'LEFTMOUSE'):
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = False
            Voxels.tool_probe_voxel(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)
            return {'FINISHED'}

             
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'FINISHED'}

        return {'RUNNING_MODAL'} 
        #return {'PASS_THROUGH'} #taken bindings seem to mess with it
    
    def invoke(self, context, event):
        if context.object:
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


class ModalOperator_voxel_set_smoothness(bpy.types.Operator):
    """set voxel smooth tool"""
    bl_idname = "object.modal_operator_set_voxel_smooth"
    bl_label = "Set voxel smooth"

    mouse_x: IntProperty()
    mouse_y: IntProperty()

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            self.mouse_x = event.mouse_region_x
            self.mouse_y = event.mouse_region_y
        
        if (event.type == 'LEFTMOUSE'):
            scene = context.scene
            voxel_menu_var = scene.voxel_menu_var
            
            add = False
            Voxels.tool_probe_set_voxel_smoothness(self.mouse_x, self.mouse_y, bpy.context.object, context, add, voxel_menu_var)
            return {'FINISHED'}

             
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'FINISHED'}

        return {'RUNNING_MODAL'} 
        #return {'PASS_THROUGH'} #taken bindings seem to mess with it
    
    def invoke(self, context, event):
        if context.object:
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


classes = [VoxelProperties, VOXEL_PT_main_panel, VOXEL_OT_add_voxel, VOXEL_OT_fill_voxel, VOXEL_OT_clear_voxel, VOXEL_OT_replace_content, VOXEL_OT_rayscan_replace_content, VOXEL_OT_foot_replace_content, VOXEL_OT_update_voxel, VOXEL_OT_add_noise, VOXEL_OT_voxify, ModalOperator_voxel_tool, ModalOperator_voxel_paint_tool, ModalOperator_voxel_paint_surface_tool, ModalOperator_voxel_probe, ModalOperator_voxel_set_smoothness]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.voxel_menu_var = bpy.props.PointerProperty(type=VoxelProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        del bpy.types.Scene.voxel_menu_var


if __name__ == "__main__":
    register()


