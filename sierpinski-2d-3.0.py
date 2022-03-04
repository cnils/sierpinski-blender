import bpy
import math
from mathutils import Vector

# pre-calculated proportions
tri_h = math.sqrt(3) / 2  # edge to top
tri_c = math.sqrt(3) / 3  # edge to center


# triangle function
def triangle(name, scale, origin=Vector((0, 0, 0))):
    # shape components
    coords = [
        origin + Vector((0, 0, 0)),
        origin + Vector((scale, 0, 0)),
        origin + Vector((scale / 2, scale * tri_h, 0))
    ]
    edges = [
    ]
    faces = [
        (0, 1, 2)
    ]

    # create new mesh and new object
    mesh = bpy.data.meshes.new(f'{name}-mesh')
    obj = bpy.data.objects.new(name, mesh)

    # make mesh from shape components
    mesh.from_pydata(coords, edges, faces)

    # show name and update the mesh
    mesh.update()

    # link object to active collection
    bpy.context.collection.objects.link(obj)

    return obj


def duplicate_move(obj, suffix, translate):
    # duplicate object
    obj2 = bpy.data.objects.new(obj.name + suffix, obj.data)

    # move object
    obj2.location += translate

    # link object to active collection
    bpy.context.collection.objects.link(obj2)

    return obj2


###########
## BEGIN ##
###########

# set iterations
iter = 8  # 8

# set sizes
size = 10
unit = size / 2 ** iter
merge_threshold = unit / 2

# offset 3d cursor
curs = bpy.context.scene.cursor.location
offset = curs + Vector((-size / 2, -size * tri_c / 2, 0))

# create base triangle
tri = triangle('Tri', unit, offset)

# iterations
for i in range(iter):

    # set base transform
    base = 2 ** i

    # set tri
    tri = bpy.data.objects['Tri']

    # duplicate/move the "object" in x-direction
    tri_x = duplicate_move(tri, '-X', Vector((base * unit, 0, 0)))
    tri_x.select_set(state=True)

    # duplicate/move the "object" on tri-direction
    tri_t = duplicate_move(tri, '-T', Vector((base * unit / 2, base * unit * tri_h, 0)))
    tri_t.select_set(state=True)

    # join all objects as "object"
    tri.select_set(state=True)
    bpy.context.view_layer.objects.active = tri
    bpy.ops.object.join()

# clean up extra vertices
# disable this for bpy.ops.mesh.select_more() to color entire tris (vs sides)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=merge_threshold)
bpy.ops.object.mode_set(mode='OBJECT')
