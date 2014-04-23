import bpy


class MyRiggingToolboxPanel(bpy.types.Panel):
    """ My rigging toolbox """
    bl_label = "My Rigging Toolbox"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        # join and separate
        col = layout.column(align=True)
        col.operator("armature.separate", text="Separate")
        col.operator("object.join", text="Join")
        
        # single bone renaming
        row = layout.row()
        row.prop(context.selected_bones[0], "name")
        row = layout.row()
        row.operator("object.renaming_operator", text="Bone renaming")
        
        # parent and unparent
        col = layout.column(align=True)
        col.operator("armature.parent_clear", text="Unparent")
        col.operator("armature.parent_set", text="Parent")
        
        # toogle names and axis
        col = layout.column(align=True)
        col.operator("object.toggle_bone_names_operator", text="Display names")
        col.operator("object.toggle_bone_axis_operator", text="Display axis")
        
        # clear location, rotation, scale
        # TODO
        
        # lock location, rotation, scale
        # TODO
        
        # color bones
        # TODO
        
        # custom controls for manipulation
        # TODO
        
        # bone mirroring
        # TODO        


def register():
    bpy.utils.register_class(MyRiggingToolboxPanel)


def unregister():
    bpy.utils.unregister_class(MyRiggingToolboxPanel)


if __name__ == "__main__":
    register()
