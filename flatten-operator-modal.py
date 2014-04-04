import bpy
import bmesh
from mathutils import Vector


class ModalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def reset_vertices(self):
        for v in self.verts:
            v.co = Vector(self.verts_backup[v.index])

    def flatten(self, context, axis):
        self.reset_vertices()
            
        min_y = min(map(lambda y : y.co[axis], self.verts))
        max_y = max(map(lambda y : y.co[axis], self.verts))
        
        old_min = min_y
        max_y += abs(min_y)
        min_y += abs(min_y)
        
        new_pos = 0.5 * (max_y - min_y)
        new_pos -= abs(old_min)
        
        for v in self.verts:
            v.co[1] = new_pos

    def modal(self, context, event):
        print(' --- MODAL --- ')
        if event.type == 'X':
            self.flatten(context, 0)
            
        elif event.type == 'Y':
            self.flatten(context, 1)
            
        elif event.type == 'Z':
            self.flatten(context, 2)
        
        elif event.type == 'ESC':
            self.reset_vertices()
            return {'CANCELLED'}
        
        elif event.type == 'ENTER':
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print(' --- INVOKE --- ')
        
        if context.active_object.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(context.active_object.data)
            self.verts = [ v for v in bm.verts if v.select ]
            self.verts_backup = {v.index : (v.co[0], v.co[1], v.co[2]) for v in bm.verts if v.select}

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalOperator)


def unregister():
    bpy.utils.unregister_class(ModalOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.modal_operator('INVOKE_DEFAULT')
