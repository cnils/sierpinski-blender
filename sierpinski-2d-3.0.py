import bpy
import math

# object name
name = 'Tri'
# set number of iterations
iter = 1  # 8

# http://i-want-to-study-engineering.org/images/tetrahedron_height_s.png
# grab object critical dimensions (assumes Tri is on xy plane with edge along x-axis)
unit_len = bpy.data.objects[name].dimensions[0]
t_h = math.sqrt(3) / 2
p_d = math.sqrt(3) / 6
p_h = math.sqrt(2 / 3)

# set 3D cursor at center
bpy.context.scene.cursor.location = (0, 0, 0)

# duplicate & hide copy of  object
sel_obj = bpy.data.objects[name]
#bpy.context.view_layer.objects.active = sel_obj
bpy.data.objects[name].select_set(True)
bpy.ops.object.duplicate_move()
bpy.context.selected_objects[0].name = name + '_backup'
bpy.data.objects[name].select_set(False)

sel_col = bpy.context.view_layer.layer_collection.children['orig']
bpy.context.view_layer.active_layer_collection.collection = sel_col
#bpy.context.scene.collection.objects.link(sel_obj)

bpy.ops.collection.objects_remove_all()

# loop
for i in range(0, iter):

    # define move parameters
    base = 2 ** i

    # move one unit in x-direction
    #bpy.data.objects[name].select_set(True)
    #bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value": (unit_len * base, 0, 0)})
    #bpy.ops.object.select_all(action='TOGGLE')

    # move one unit in tri-direction
    #bpy.data.objects[name].select_set(True)
    #bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value": (0.5 * unit_len * base, t_h * unit_len * base, 0)})
    #bpy.ops.object.select_all(action='TOGGLE')

    # join transformation objects and reset name
    #bpy.context.view_layer.objects.active = bpy.data.objects[name]
    #bpy.ops.object.select_all(action='TOGGLE')
    #bpy.ops.object.join()
  
# set the origin to 3D cursor location
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')