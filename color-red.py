bl_info = {
           'name':'Color bones',
           'category':'User',
           'author':'miguel'
           }

import bpy
from mathutils import Color


class ColorBoneOperator(bpy.types.Operator):
    """ Color selected bones """
    bl_idname = "object.color_bone_operator"
    bl_label = "Color selected bones" 
    color = bpy.props.StringProperty(name='color')
    
    def execute(self, context):
        
        # get selected object
        obj = context.scene.objects.active
        armature = context.active_object
        
        # get actual mode
        orig_mode = armature.mode
        
        # switch pose mode
        bpy.ops.object.mode_set(mode='POSE')
        
        # check if a bone group already exists
        orig_actual_bg_name = None
        if obj.pose.bone_groups.active != None:
        
            # get actual bone group
            orig_actual_bg_name = obj.pose.bone_groups.active.name
        
        # check if red group already exists
        if not ColorBoneOperator.color in obj.pose.bone_groups:
        
            # if not create new group
            bpy.ops.pose.group_add()
            
            # get new group
            grp = obj.pose.bone_groups.active
            
            # rename group
            grp.name = ColorBoneOperator.color
            
            # set color of group
            if ColorBoneOperator.color == 'red':
                grp.colors.normal = Color((1.0, 0.0, 0.0))
            else:
                grp.colors.normal = Color((0.0, 0.0, 1.0))
                
            grp.colors.select = Color((0.0, 0.0, 0.0))
            grp.colors.active = Color((0.5, 0.5, 0.5))
                
        
        # grap red group
        grp = obj.pose.bone_groups[ColorBoneOperator.color]
        
        # set color to CUSTOM
        grp.color_set = 'CUSTOM'
        
        # assign bones to group
        bpy.ops.pose.group_assign(type=1)
        
        # restore actual bone group
        if orig_actual_bg_name != None:
            orig_bg = obj.pose.bone_groups[orig_actual_bg_name]
            obj.pose.bone_groups.active = orig_bg
        
        # restore mode
        bpy.ops.object.mode_set(mode=orig_mode)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ColorBoneOperator)


def unregister():
    bpy.utils.unregister_class(ColorBoneOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.color_bone_operator()
