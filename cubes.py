import bpy
import random

spacing = 2.2
for x in range(10):
    for y in range(10):
        location = (x * spacing, y * spacing, random.random() *2)
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode = False, align = 'WORLD', location=location, scale=(1,1,1))