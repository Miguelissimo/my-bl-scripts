bl_info = {
           'name':'MakeParentEmpty',
           'category':'User',
           'author':'miguel'
           }

import bpy
from mathutils import Vector, Euler


class MakeEmptyParentOperator(bpy.types.Operator):
    """ takes the actual object and makes it a child of a new empty """
    bl_idname = "object.make_empty_parent_operator"
    bl_label = "Make Empty Parent Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        # current object in edit mode
        obj = context.active_object
        if not obj.mode == 'OBJECT':
            return {'CANCELLED'}
        
        # save obj coordinates
        orig_loc = obj.location.copy()
        orig_rot = obj.rotation_euler.copy()
        orig_sca = obj.scale.copy()
        
        # set object to (0,0,0)
        obj.location = Vector((0,0,0))
        obj.rotation_euler = Euler((0,0,0), 'XYZ')
        obj.scale = Vector((1,1,1))
        
        # create emtpy
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        
        # get newly creted object
        empty = context.active_object
        
        # hide empty
        empty.hide = True
        
        # parent obj under empty
        obj.parent = empty
        
        # move empty to old location
        empty.location = orig_loc
        empty.rotation_euler = orig_rot
        empty.scale = orig_sca
        
        print('location %s ' % str(orig_loc))
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MakeEmptyParentOperator)


def unregister():
    bpy.utils.unregister_class(MakeEmptyParentOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.make_empty_parent_operator()