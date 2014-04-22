import bpy
import bgl
import blf
from mathutils import Vector


class DrawTextOperator(bpy.types.Operator):
    bl_idname = "object.draw_text_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        sel_obj_loc = context.active_object.location
        
        # draw hello world
        font_id = 0
        blf.position(font_id, 512, 512, 0)
        blf.size(font_id, 50, 72)
        blf.draw(font_id, "Hello World")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(DrawTextOperator)


def unregister():
    bpy.utils.unregister_class(DrawTextOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.draw_text_operator()

