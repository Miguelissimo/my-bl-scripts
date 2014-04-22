import bpy
import bgl
import blf


def draw_callback_px(self, context):

    font_id = 0  # XXX, need to find out how best to get this.

    # draw some text
    bgl.glColor4f(1, 1, 1, 1)
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, self.key)


    # restore opengl defaults
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class ModalDrawOperator(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal View3D Operator"

    def modal(self, context, event):

        mod = []
        if event.shift:
            mod.append("Shift")
        if event.alt:
            mod.append("Alt")
        if event.ctrl:
            mod.append("Ctrl")

        if mod:
            mod = "[%s]" % "+".join(mod)
        else:
            mod = ""

        context.area.header_text_set("%s %s - %s" % (mod, event.type, event.value))

        if event.unicode:
            self.key += event.unicode
            context.area.tag_redraw()

        elif event.type in {'RET', 'NUMPAD_ENTER', 'BACK_SPACE', 'DEL'}:
            self.key = ""
            context.area.tag_redraw()

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            context.area.tag_redraw()
            context.area.header_text_set()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            self.key = ""

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalDrawOperator)


def unregister():
    bpy.utils.unregister_class(ModalDrawOperator)

if __name__ == "__main__":
    register()