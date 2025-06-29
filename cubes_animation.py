import bpy, random, mathutils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

spacing      = 2.2
grid_size    = 10
start_frame  = 1
end_frame    = 0             
bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end   = end_frame

for x in range(grid_size):
    for y in range(grid_size):
        height = random.uniform(0.5, 2.5)

        # Add cube
        loc = (x * spacing, y * spacing, height / 2)
        bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
        cube = bpy.context.object

        cube.scale.z = 0.001
        cube.keyframe_insert(data_path="scale", frame=start_frame)

        cube.scale.z = height / 2        
        cube.keyframe_insert(data_path="scale", frame=end_frame)

        if "GrayMat" not in bpy.data.materials:
            gmat = bpy.data.materials.new("GrayMat")
            gmat.use_nodes = True
            gmat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)
            gmat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.45
        cube.data.materials.append(bpy.data.materials["GrayMat"])

bpy.ops.object.light_add(type='POINT', location=(-5, -5, 15))
light = bpy.context.object
light.data.energy          = 1500
light.data.shadow_soft_size = 0.5

cam_loc = (spacing * 5, -spacing * 14, spacing * 6)
bpy.ops.object.camera_add(location=cam_loc)
camera = bpy.context.object

target = mathutils.Vector((spacing * (grid_size - 1) / 2,
                           spacing * (grid_size - 1) / 2,
                           1))          
camera.rotation_euler = (target - camera.location)\
                        .to_track_quat('-Z', 'Y').to_euler()

bpy.context.scene.camera = camera

scene = bpy.context.scene
scene.render.engine                = 'CYCLES'
scene.cycles.samples               = 64
scene.render.resolution_x          = 1920
scene.render.resolution_y          = 1080
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.0
