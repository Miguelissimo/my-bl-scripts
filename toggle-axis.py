import bpy


class ToggleAxisOperator(bpy.types.Operator):
    """ Display toggle for bone names"""
    bl_idname = "object.toggle_bone_axis_operator"
    bl_label = "Toggle Bone Axis Operator"

    def execute(self, context):
        context.object.data.show_axes = not context.object.data.show_axes
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ToggleAxisOperator)


def unregister():
    bpy.utils.unregister_class(ToggleAxisOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.toggle_bone_axis_operator()
