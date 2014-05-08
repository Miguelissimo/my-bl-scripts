bl_info = {
           'name':'MyRiggingToolbox',
           'category':'User',
           'author':'miguel'
           }

import bpy


class MyRiggingToolboxPanel(bpy.types.Panel):
    """ My rigging toolbox """
    bl_label = "My Rigging Toolbox"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        # save incremental
        row = layout.row()
        row.operator("object.save_incremental", text="Save++")
        
        # join and separate
        col = layout.column(align=True)
        col.operator("armature.duplicate", text="Duplicate")
        col.operator("armature.separate", text="Separate")
        col.operator("object.join", text="Join")
        col.operator("armature.align", text="Align")
        
        # parent and unparent
        col = layout.column(align=True)
        col.operator("armature.parent_clear", text="Unparent")
        col.operator("armature.parent_set", text="Parent")
        
        # single bone renaming
        row = layout.row()
        if context.selected_bones != None:
            row.prop(context.selected_bones[0], "name")
            row = layout.row()
        row.operator("object.renaming_operator", text="Bone renaming")
        
        # toogle names and axis
        col = layout.column(align=True)
        col.operator("object.toggle_bone_names_operator", text="Display names")
        col.operator("object.toggle_bone_axis_operator", text="Display axis")
        # TODO toggle color
        
        # parent under null but keep location, rotation, scale
        row = layout.row()
        row.operator("object.make_empty_parent_operator", text="Parent under Empty")
        
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
