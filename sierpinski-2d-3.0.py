import bpy
import math

# pre-calculated lengths
t_h = math.sqrt(3) / 2


# triangle function
def triangle(name, scale, edges=[], faces=[]):
    # shape components
    coords = [
        (0, 0, 0),
        (scale, 0, 0),
        (scale / 2, scale * t_h ,0)
    ]
    faces = [
        (0, 1, 2)
    ]

    # create new mesh and new object
    mesh = bpy.data.meshes.new(f'{name}-Mesh')
    obj = bpy.data.objects.new(name, mesh)

    # make mesh from shape components
    mesh.from_pydata(coords, edges, faces)

    # show name and update the mesh
    #obj.show_name = True
    mesh.update()
    
    # link object to active collection
    bpy.context.collection.objects.link(obj)
    
    return obj


def duplicate_move(obj, suffix, new_location):
    # duplicate object
    obj2 = bpy.data.objects.new(obj.name + suffix, obj.data)
    
    # move object
    obj2.location = new_location
    
    # link object to active collection
    bpy.context.collection.objects.link(obj2)
    
    return obj2


###########
## BEGIN ##
###########

# set iterations
iter = 8

# set sizes
size = 10
unit = size / 2 ** iter

# create base triangle
tri = triangle('Tri', unit)

# iterations
for i in range(iter):

    # set base transform
    base = 2 ** i
    
    # set tri
    tri = bpy.data.objects['Tri']
    
    # duplicate/move the "object" in x-direction
    tri_x = duplicate_move(tri, '-X', (base * unit, 0, 0))
    tri_x.select_set(state=True)
    
    # duplicate/move the "object" on tri-direction
    tri_t = duplicate_move(tri, '-T', (0.5 * base * unit, t_h * base * unit, 0))
    tri_t.select_set(state=True)
    
    # join all objects as "object"
    tri.select_set(state=True)
    bpy.context.view_layer.objects.active = tri
    bpy.ops.object.join()