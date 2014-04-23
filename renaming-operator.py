import bpy
import string
import time


class RenamingOperator(bpy.types.Operator):
    """ Interactive renaming tool """
    bl_idname = "object.renaming_operator"
    bl_label = "Renaming Tool"

    def add_char(self, context, c):
        if context.active_bone == None:
            return {'RUNNING_MODAL'}
        else:
            if context.active_bone != self.current_bone:
                self.orig_bone_name = context.active_bone.name
                self.current_bone = context.active_bone
                self.clear_bone_name()
                self.has_orig_name = True
                print('orig_bone_name: %s' % self.orig_bone_name)
            
            if self.has_orig_name:
                self.current_bone.name = c
                self.has_orig_name = False
            else:    
                self.current_bone.name += c
            return {'RUNNING_MODAL'}
    
    def clear_bone_name(self):
        bone_name = ''
        
    def modal(self, context, event):        
        if event.type in {'RET', 'NUMPAD_ENTER'}:
            print('EXIT')
            return {'FINISHED'}
        
        if event.unicode != '' and event.unicode in self.registered_characters:
            return self.add_char(context, '%s' % event.unicode)
        
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        print('INVOKE')
        self.orig_bone_name = ''
        self.current_bone = None
        self.has_orig_name = True
        
        self.registered_characters = string.ascii_lowercase
        self.registered_characters += string.ascii_uppercase
        self.registered_characters += string.digits
        self.registered_characters += '_.'
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(RenamingOperator)


def unregister():
    bpy.utils.unregister_class(RenamingOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.renaming_operator('INVOKE_DEFAULT')
