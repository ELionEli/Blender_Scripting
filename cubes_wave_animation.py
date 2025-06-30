import bpy, random, math, mathutils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

spacing     = 2.2
grid_size   = 10
start_frame = 1
end_frame   = 120
bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end   = end_frame

center_x = spacing * (grid_size - 1) / 2
center_y = spacing * (grid_size - 1) / 2

for x in range(grid_size):
    for y in range(grid_size):
        dist = math.hypot(x - grid_size / 2, y - grid_size / 2)
        delay = dist * 2.5  # distance from center
        base_height = random.uniform(1.0, 2.0)
 
        # adds cube:
        z_pos = base_height / 2
        location = (x * spacing, y * spacing, z_pos)
        bpy.ops.mesh.primitive_cube_add(size=2, location=location)
        cube = bpy.context.object

        # wave animation
        for f in range(start_frame, end_frame + 1, 5):
            wave = math.sin((f - delay) * 0.15)
            height = base_height + wave * 1.0
            cube.scale.z = max(0.1, height / 2)
            cube.location.z = cube.scale.z  # move the cube to keep bottom on the ground
            cube.keyframe_insert(data_path="scale", frame=f)
            cube.keyframe_insert(data_path="location", frame=f)

        # simple neutral material
        if "GrayMat" not in bpy.data.materials:
            gmat = bpy.data.materials.new("GrayMat")
            gmat.use_nodes = True
            bsdf = gmat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)
            bsdf.inputs["Roughness"].default_value = 0.45
        cube.data.materials.append(bpy.data.materials["GrayMat"])

# light
bpy.ops.object.light_add(type='POINT', location=(-5, -5, 15))
light = bpy.context.object
light.data.energy = 1500
light.data.shadow_soft_size = 0.5

# camera
cam_loc = (spacing * 5, -spacing * 14, spacing * 6)
bpy.ops.object.camera_add(location=cam_loc)
camera = bpy.context.object
target = mathutils.Vector((center_x, center_y, 1))
camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = camera

# render
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.0


