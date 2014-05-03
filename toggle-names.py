bl_info = {
           'name':'ToogleNames',
           'category':'User',
           'author':'miguel'
           }

import bpy


class ToggleNamesOperator(bpy.types.Operator):
    """ Display toggle for bone names"""
    bl_idname = "object.toggle_bone_names_operator"
    bl_label = "Toggle Bone Name Operator"

    def execute(self, context):
        context.object.data.show_names = not context.object.data.show_names
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ToggleNamesOperator)


def unregister():
    bpy.utils.unregister_class(ToggleNamesOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.toggle_bone_names_operator()
