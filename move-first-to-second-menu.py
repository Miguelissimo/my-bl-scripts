bl_info = {
           'name':'Move first to second menu',
           'category':'User',
           'author':'miguel'
           }

import bpy

HEAD = 1
TAIL = 2

def _move_bone(head_or_tail):
    armature = context.active_object
    dest_bone = context.active_bone
    
    # find dest bone
    src_bone = None
    for bone in armature.data.edit_bones:
        if bone.select and bone != dest_bone:
            src_bone = bone
        
    if src_bone == None:
        print('Needs two bones selected')
        return {'CANCELLED'}
    
    if head_or_tail == 1:
        target_pos = dest_bone.head.copy()
    else:
        target_pos = dest_bone.tail.copy()
        
    src_bone_head = src_bone.head.copy()
    src_bone_tail = src_bone.tail.copy()
    
    src_bone.head = target_pos
    
    dir_vec = -src_bone_head + src_bone_tail
    src_bone.tail = target_pos + dir_vec


class MoveBoneToTail(bpy.types.Operator):
    """ Move first selected bone to tail of second"""
    bl_idname = "object.move_bone_to_tail_operator"
    bl_label = "Move bone to tail Operator"

    def execute(self, context):
        _move_bone(2)
        return {'FINISHED'}

class MoveBoneToHead(bpy.types.Operator):
    """ Move first selected bone to tail of second"""
    bl_idname = "object.move_bone_to_head_operator"
    bl_label = "Move bone to head Operator"

    def execute(self, context):
        _move_bone(1)
        return {'FINISHED'}

class MoveFirstSecondMenu(bpy.types.Menu):
    bl_label = "Move first selected bone to second menu"
    bl_idname = "View3D.MoveFirstSecondMenu"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("object.move_bone_to_tail_operator", text='Bone to tail')
        layout.operator("object.move_bone_to_head_operator", text='Bone to head')
        
def register():
    bpy.utils.register_class(MoveBoneToHead)
    bpy.utils.register_class(MoveBoneToTail)
    bpy.utils.register_class(MoveFirstSecondMenu)
    
        
def unregister():
    bpy.utils.unregister_class(MoveFirstSecondMenu)
    bpy.utils.register_class(MoveBoneToTail)
    bpy.utils.unregister_class(MoveBoneToHead)
    
        
if __name__ == '__main__':
    register()
    bpy.ops.wm.call_menu(name=MoveFirstSecondMenu.bl_idname)