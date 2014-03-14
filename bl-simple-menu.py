import bpy

# Hello

class customMenu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "View3D.custom_menu"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("mesh.primitive_cube_add")
        
def register():
    bpy.utils.register_class(customMenu)
    bpy.ops.wm.call_menu(name=customMenu.bl_idname)
        
def unreister():
    bpy.utils.unregister_class(customMenu)
        
if __name__ == '__main__':
    register()