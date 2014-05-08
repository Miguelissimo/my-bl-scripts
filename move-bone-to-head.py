import bpy

class MoveBoneToHead(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.move_bone_to_head_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        
        bone = context.active_bone
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MoveBoneToHead)


def unregister():
    bpy.utils.unregister_class(MoveBoneToHead)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.move_bone_to_head_operator()
