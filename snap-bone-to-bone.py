
import bpy

class SnapBoneToBone(bpy.types.operator):
    """ snaps src bone to dest bone """
    bl_idname = "object.snap_bone_to_bone"
    bl_label = "Snap Bone to Bone"
    
    def execute(self, context):
        obj = context.active_object
        if obj.mode == 'EDIT':
            pass
        else:
            self.report({'WARNING'}, "Object is not in edit mode")
            return {'CANCELLED'}
    

def register():
    bpy.utils.register(SnapBoneToBone)

def unregister():
    bpy.utils.unregister(SnapBoneToBone)

if __name__ == '__main__':
    register()
    
    # test call
    bpy.ops.snap_bone_to_bone()