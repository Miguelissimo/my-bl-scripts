import bpy
from mathutils import Vector

obj = bpy.context.active_object
print(obj)

pos = obj.location

# get current frame
cf = bpy.context.scene.frame_current

# set current frame
bpy.context.scene.frame_current = 1

#insert key, e.g. on location
obj.keyframe_insert(data_path='location', frame=1)

obj.location = Vector((0,5,0))

obj.keyframe_insert(data_path='location', frame=20)

# animation start
bpy.ops.screen.animation_play()

# animation stop
bpy.ops.screen.animation_cancel()