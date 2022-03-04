import bpy
import math
from mathutils import Vector

# pre-calculated proportions
tri_h = math.sqrt(3) / 2  # edge to top
tri_c = math.sqrt(3) / 3  # edge to center
tet_v = math.sqrt(3) / 6  # edge to face center for vertex above
tet_h = math.sqrt(2 / 3)  # face to top
tet_c = math.sqrt(3 / 8)  # face to center

# triangle function
def tetrahedron(name, scale, origin=Vector((0, 0, 0))):
    # shape components
    coords = [
        origin + Vector((0, 0, 0)),
        origin + Vector((scale, 0, 0)),
        origin + Vector((scale / 2, scale * tri_h, 0)),
        origin + Vector((scale / 2, scale * tet_v, scale * tet_h))
    ]
    edges = [
    ]
    faces = [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3)
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
offset = curs + Vector((-size / 2, -size * tri_c / 2, -size * tet_c / 2))

# create base triangle
tet = tetrahedron('Tet', unit, offset)

# iterations
for i in range(iter):

    # set base transform
    base = 2 ** i

    # set tri
    tet = bpy.data.objects['Tet']

    # duplicate/move the "object" in x-direction
    tet_x = duplicate_move(tet, '-X', Vector((base * unit, 0, 0)))
    tet_x.select_set(state=True)

    # duplicate/move the "object" on tri-direction
    tet_t = duplicate_move(tet, '-TRI', Vector((base * unit / 2, base * unit * tri_h, 0)))
    tet_t.select_set(state=True)

    # duplicate/move the "object" on tet-direction
    tet_tt = duplicate_move(tet, '-TET', Vector((base * unit / 2, base * unit * tet_v, base * unit * tet_h)))
    tet_tt.select_set(state=True)

    # join all objects as "object"
    tet.select_set(state=True)
    bpy.context.view_layer.objects.active = tet
    bpy.ops.object.join()

# clean up extra vertices
# disable this for bpy.ops.mesh.select_more() to color entire tetras (vs sides)
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.remove_doubles(threshold=merge_threshold)
#bpy.ops.object.mode_set(mode='OBJECT')
