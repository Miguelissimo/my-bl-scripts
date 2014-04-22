import bpy
import bgl
import blf
import bpy_extras

from mathutils import Vector
from bpy.props import StringProperty, FloatProperty
from bpy_extras import view3d_utils

'''
    helper functions 
'''

def get_objects(context):

    sel_obs = context.selected_objects        
    names = [object.name for object in sel_obs if object.type=='EMPTY']
    if len(names) == 2: 
        return names
    else: 
        return None
    

def get_distance(names_of_empties):

    if names_of_empties == None:
        return 0.0

    coordlist = []
    for name in names_of_empties:
        coordlist.append(bpy.data.objects[name].location)

    return (coordlist[0]-coordlist[1]).length


def get_distance_from_context(context):
    distance = get_distance(get_objects(context))
    return distance


def get_coordinates_from_empties(object_list):
    coordlist = [obj.location for obj in object_list]
    return coordlist


def get_difference(axis, coord):
    
    if axis == 'z':
        return abs((coord[0]-coord[1]).z)
    elif axis == 'y':
        return abs((coord[0]-coord[1]).y)
    elif axis == 'x':
        return abs((coord[0]-coord[1]).x)
    else:
        return None


def return_sorted_coordlist(coords):
    def MyFn(coord):  
        return coord.z
    return sorted(coords, key=MyFn, reverse=True)
            

'''
    openGL drawing
'''


def draw_text(col, y_pos, display_text, view_width, context):

    # calculate text width, then draw
    font_id = 0
    blf.size(font_id, 18, 72)  #fine tune
    
    text_width, text_height = blf.dimensions(font_id, display_text)
    right_align = view_width-text_width-18
    blf.position(font_id, right_align, y_pos, 0)
    blf.draw(font_id, display_text)
    return


def draw_tetrahedron(region, rv3d, context, clist):
   
    # highest point is apex
    apex, baseco = return_sorted_coordlist(clist)
        
    # define the base of the tetrahydron
    base1 = Vector((apex.x, apex.y, baseco.z))
    base2 = Vector((apex.x, baseco.y, baseco.z))
    base3 = baseco
    
    # converting to screen coordinates
    screen_apex = view3d_utils.location_3d_to_region_2d(region, rv3d, apex)
    screen_base1 = view3d_utils.location_3d_to_region_2d(region, rv3d, base1) 
    screen_base2 = view3d_utils.location_3d_to_region_2d(region, rv3d, base2)
    screen_base3 = view3d_utils.location_3d_to_region_2d(region, rv3d, base3)
        
    # bgl.glBegin(bgl.GL_LINE)
    
    # colour + line setup, 50% alpha, 1 px width line
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0.1, 0.3, 1.0, 0.8)
    bgl.glLineWidth(1)
    
    # from top to base coordinates
    bgl.glColor4f(0.6, 0.6, 0.6, 0.8)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(*screen_apex)  
    bgl.glVertex2f(*screen_base3)  
    bgl.glEnd()

    bgl.glColor4f(0.1, 0.3, 1.0, 0.8)
    bgl.glBegin(bgl.GL_LINES)  
    bgl.glVertex2f(*screen_apex)  
    bgl.glVertex2f(*screen_base1)  
    bgl.glEnd()
    
    bgl.glColor4f(0.1, 0.3, 1.0, 0.2)
    bgl.glBegin(bgl.GL_LINES)  
    bgl.glVertex2f(*screen_apex)  
    bgl.glVertex2f(*screen_base2)  
    bgl.glEnd()
    
    # between base coordinates
    bgl.glColor4f(1.0, 0.1, 0.1, 0.8)
    bgl.glBegin(bgl.GL_LINES)  
    bgl.glVertex2f(*screen_base3)  
    bgl.glVertex2f(*screen_base2)
    bgl.glEnd()

    bgl.glColor4f(0.0, 1.0, 0.1, 0.8)    
    bgl.glBegin(bgl.GL_LINES)  
    bgl.glVertex2f(*screen_base2)
    bgl.glVertex2f(*screen_base1)  
    bgl.glEnd()
    
    bgl.glColor4f(0.1, 0.3, 1.0, 0.2)
    bgl.glBegin(bgl.GL_LINES)  
    bgl.glVertex2f(*screen_base1)  
    bgl.glVertex2f(*screen_base3)  
    bgl.glEnd()
  
    
    return


def draw_callback_px(self, context):
    rounding = 6
    
    objlist = context.selected_objects
    names_of_empties = [i.name for i in objlist]
    distance_value = get_distance(names_of_empties)
    coordinate_list = get_coordinates_from_empties(objlist)
     
    region = bpy.context.region
    rv3d = bpy.context.space_data.region_3d
    view_width = context.region.width
    
    # major rewrite candidate
    l_distance = str(round(distance_value, rounding))
    x_distance = round(get_difference('x', coordinate_list),rounding)
    y_distance = round(get_difference('y', coordinate_list),rounding)
    z_distance = round(get_difference('z', coordinate_list),rounding)
    l_distance = str(l_distance)+" lin"
    x_distance = str(x_distance)+" x"
    y_distance = str(y_distance)+" y"            
    z_distance = str(z_distance)+" z"
    
    y_heights = 88, 68, 48, 20
    y_heights = [m-9 for m in y_heights]  # fine tune
    
    str_dist = x_distance, y_distance, z_distance, l_distance
    for i in range(len(y_heights)):
        draw_text(True, y_heights[i], str_dist[i], view_width, context)
    
    # 50% alpha, 2 pixel width line
    bgl.glEnable(bgl.GL_BLEND)
    
    bgl.glColor4f(0.7, 0.7, 0.7, 0.5)
    bgl.glLineWidth(1)
    
    bgl.glBegin(bgl.GL_LINE_STRIP)
    for coord in coordinate_list:
        vector3d = (coord.x, coord.y, coord.z)
        vector2d = view3d_utils.location_3d_to_region_2d(region, rv3d, vector3d)
        bgl.glVertex2f(*vector2d)
    bgl.glEnd()

    draw_tetrahedron(region, rv3d, context, coordinate_list)

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)



'''
    tool panel and button definitions
'''


class ToolPropsPanel(bpy.types.Panel):
    bl_label = "Empties Calliper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    scn = bpy.types.Scene
    ctx = bpy.context

    @classmethod
    def poll(self, context):
        names_of_empties = get_objects(context)
        if names_of_empties != None:
            return True

    def draw(self, context):

        display_distance_field = False
        
        layout = self.layout
        scn = context.scene

        names_of_empties = get_objects(context)
        names_str = str(names_of_empties) 
                
        if names_of_empties != None:
            display_distance_field = True
            distance_value = get_distance(names_of_empties)


        distance_value = str(distance_value)
        
        # drawing        
        row1 = layout.row(align=True)
        row1.operator("hello.hello", text=names_str)

        if display_distance_field == True:
            row3 = layout.row(align=True)
            row3.label(distance_value)


class OBJECT_OT_HelloButton(bpy.types.Operator):
    bl_idname = "hello.hello"
    bl_label = "Say Hello"
    
    def modal(self, context, event):
        context.area.tag_redraw()
    
        if event.type == 'MOUSEMOVE':
            print("mouse moved")
        elif event.type in ('RIGHTMOUSE', 'ESC'):
            context.region.callback_remove(self._handle)
            return {'CANCELLED'}
    
        return {'RUNNING_MODAL'}
     
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = context.region.callback_add(
                            draw_callback_px, 
                            (self, context), 
                            'POST_PIXEL')

            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, 
            "View3D not found, cannot run operator")
            
        return {'CANCELLED'}

    

bpy.utils.register_module(__name__)

