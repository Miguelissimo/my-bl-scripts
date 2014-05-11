import bpy

class MoveBoneToHead(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.move_bone_to_head_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        
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
        
        target_pos = dest_bone.tail.copy()
        src_bone_head = src_bone.head.copy()
        src_bone_tail = src_bone.tail.copy()
        
        src_bone.head = target_pos
        
        dir_vec = -src_bone_head + src_bone_tail
        src_bone.tail = target_pos + dir_vec
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MoveBoneToHead)


def unregister():
    bpy.utils.unregister_class(MoveBoneToHead)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.move_bone_to_head_operator()
