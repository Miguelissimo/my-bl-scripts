import bpy
import bmesh
from mathutils import Vector


class FlattenOperator(bpy.types.Operator):
    """ flattens selected vertices on a given axis"""
    bl_idname = "object.flatten_operator"
    bl_label = "Flatten Operator"

    def reset_vertices(self):
        for v in self.verts:
            v.co = Vector(self.verts_backup[v.index])

    def flatten(self, context, axis):
        self.reset_vertices()
            
        min_v = min(map(lambda v : v.co[axis], self.verts))
        max_v = max(map(lambda v : v.co[axis], self.verts))
        
        old_min = min_v
        max_v += abs(min_v)
        min_v += abs(min_v)
        
        new_pos = 0.5 * (max_v - min_v)
        new_pos -= abs(old_min)
        
        for v in self.verts:
            v.co[axis] = new_pos
        
        bmesh.update_edit_mesh(context.active_object.data)
        
    def modal(self, context, event):
        if event.type == 'X':
            self.flatten(context, 0)
            
        elif event.type == 'Y':
            self.flatten(context, 1)
            
        elif event.type == 'Z':
            self.flatten(context, 2)
        
        elif event.type == 'ESC':
            self.reset_vertices()
            bmesh.update_edit_mesh(context.active_object.data)
            return {'CANCELLED'}
        
        elif event.type == 'SPACE':
            return {'FINISHED'}
        
        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        
        if context.active_object.mode == 'EDIT':
            self.bm = bmesh.from_edit_mesh(context.active_object.data)
            self.verts = [ v for v in self.bm.verts if v.select ]
            self.verts_backup = {v.index : (v.co[0], v.co[1], v.co[2]) for v in self.bm.verts if v.select}

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(FlattenOperator)


def unregister():
    bpy.utils.unregister_class(FlattenOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.flatten_operator('INVOKE_DEFAULT')
