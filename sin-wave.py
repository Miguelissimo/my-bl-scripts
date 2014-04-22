
import bpy
import bmesh
from math import *

APLITUDE = 10

obj = bpy.context.active_object
bm = bmesh.from_edit_mesh(obj.data)

for v in bm.verts:
    x, y, z = v.co
    
    v.co[2] = sin(v.co[0]) * APLITUDE
    
bmesh.update_edit_mesh(bpy.context.active_object.data)