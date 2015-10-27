import bpy
import math

# object name
name = 'Tet'
# set number of iterations
iter = 3

# tetrahedron variables
# http://i-want-to-study-engineering.org/images/tetrahedron_height_s.png
unit_len = 1
t_h = math.sqrt(3)/2
p_d = math.sqrt(3)/6
p_h = math.sqrt(2/3)

# build Tet object and place in scene
verts = [(0, 0, 0), (1, 0, 0), (0.5, t_h, 0), (0.5, p_d, p_h)]
faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
mesh_data = bpy.data.meshes.new(str(name)+'-mesh')
mesh_data.from_pydata(verts, [], faces)
mesh_data.update()
obj = bpy.data.objects.new(name, mesh_data)
scene = bpy.context.scene
scene.objects.link(obj)

# set 3D cursor at center
bpy.context.scene.cursor_location = (0,0,0)

# duplicate & hide copy of  object
bpy.data.objects[name].select = True
bpy.ops.object.duplicate_move()
bpy.context.selected_objects[0].name = 'backup'
bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False))

# loop
for i in range(0,iter):

    # define move parameters
    base = 2**(i)

    # move one unit in x-direction
    bpy.data.objects[name].select = True
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(unit_len * base, 0, 0)})
    bpy.ops.object.select_all(action='TOGGLE')

    # move one unit in tri-direction
    bpy.data.objects[name].select = True
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(0.5 * unit_len * base, t_h * unit_len * base, 0)})
    bpy.ops.object.select_all(action='TOGGLE')
    
    # move one unit in tet-direction
    bpy.data.objects[name].select = True
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(0.5 * unit_len * base, p_d * unit_len * base, p_h * unit_len * base)})
    bpy.ops.object.select_all(action='TOGGLE')

    # join transformation objects and reset name
    bpy.context.scene.objects.active = bpy.data.objects[name]
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.join()
  
# set the origin to 3D cursor location
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
