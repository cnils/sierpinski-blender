import bpy
import math

p_h = math.sqrt(2 / 3)

def triangle(name, scale, edges=[], faces=[]):
    coords = [
        (0, 0, 0),
        (scale, 0, 0),
        (scale / 2, scale * p_h ,0)
    ]
    faces = [
        (0,1,2)
    ]

    # Create new mesh and a new object
    mesh = bpy.data.meshes.new(f'{name}-Mesh')
    obj = bpy.data.objects.new(name, mesh)

    # Make a mesh from a list of vertices/edges/faces
    mesh.from_pydata(coords, edges, faces)

    # Display name and update the mesh
    obj.show_name = True
    mesh.update()
    return obj

# Create the object
tri = triangle('Tri', 1)

# Link object to the active collection
bpy.context.collection.objects.link(tri)

# Alternatively Link object to scene collection
#bpy.context.scene.collection.objects.link(tri)

# Try a second object
tri2 = bpy.data.objects.new('Tri2', bpy.data.objects['Tri'].data)
tri2.location = (1,0,0)
bpy.context.collection.objects.link(tri2)


###########
## BEGIN ##
###########

# create base triangle

# deselect triangle

# iterations

    # set base transform
    
    # duplicate/move the "object" in x-direction
    
    # duplicate/move the "object" on tri-direction
    
    # join all objects as "object"