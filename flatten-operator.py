import bpy
import bmesh

def flatten(context, axis):
    obj = context.active_object
    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(obj.data)
        verts = [v for v in bm.verts if v.select]
        
        min_y = min(map(lambda y : y.co[axis], verts))
        max_y = max(map(lambda y : y.co[axis], verts))
        
        old_min = min_y
        max_y += abs(min_y)
        min_y += abs(min_y)
        
        new_pos = 0.5 * (max_y - min_y)
        new_pos -= abs(old_min)
        
        for v in verts:
            v.co[1] = new_pos

def main(context):
    flatten(context, 1)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
