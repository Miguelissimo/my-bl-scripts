import bpy
from mathutils import Color


class ColorBoneRedOperator(bpy.types.Operator):
    """ Color selected bones red """
    bl_idname = "object.color_bone_red_operator"
    bl_label = "Color selected bones red"

    def execute(self, context):
        
        # get selected object
        obj = context.scene.objects.active
        
        # get actual mode
        orig_mode = obj.mode
        
        # switch pose mode
        bpy.ops.object.mode_set(mode='POSE')
        
        # check if a bone group already exists
        orig_actual_bg_name = None
        if obj.pose.bone_groups.active != None:
        
            # get actual bone group
            orig_actual_bg_name = obj.pose.bone_groups.active.name
        
        # check if red group already exists
        if not 'red' in obj.pose.bone_groups:
        
            # if not create new group
            bpy.ops.pose.group_add()
            
            # get new group
            grp = obj.pose.bone_groups.active
            
            # rename group
            grp.name = 'red'
            
            # set color of group
            grp.colors.normal = Color((1.0, 0.0, 0.0))
            grp.colors.select = Color((0.0, 0.0, 0.0))
            grp.colors.active = Color((0.5, 0.5, 0.5))
        
        # grap red group
        grp = obj.pose.bone_groups['red']
        
        # set color to CUSTOM
        grp.color_set = 'CUSTOM'
        
        # assign bones to group
        bpy.ops.pose.group_assign(type=2)
        
        # restore actual bone group
        orig_bg = obj.pose.bone_groups[orig_actual_bg_name]
        obj.pose.bone_groups.active = orig_bg
        
        # restore mode
        bpy.ops.object.mode_set(mode=orig_mode)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ColorBoneRedOperator)


def unregister():
    bpy.utils.unregister_class(ColorBoneRedOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.color_bone_red_operator()
