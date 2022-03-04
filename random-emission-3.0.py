import bpy
import bmesh
from random import choice 

# create emission material (as secondary)
# https://vividfax.github.io/2021/01/14/blender-materials.html
def newMaterial(id):
    mat = bpy.data.materials.get(id)

    if mat is None:
        mat = bpy.data.materials.new(name=id)

    mat.use_nodes = True

    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()

    return mat

def newShader(id, type, r, g, b):
    mat = newMaterial(id)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')

    if type == 'diffuse':
        shader = nodes.new(type='ShaderNodeBsdfDiffuse')
        nodes['Diffuse BSDF'].inputs[0].default_value = (r, g, b, 1)

    elif type == 'emission':
        shader = nodes.new(type='ShaderNodeEmission')
        nodes['Emission'].inputs[0].default_value = (r, g, b, 1)
        nodes['Emission'].inputs[1].default_value = 1

    elif type == 'glossy':
        shader = nodes.new(type='ShaderNodeBsdfGlossy')
        nodes['Glossy BSDF'].inputs[0].default_value = (r, g, b, 1)
        nodes['Glossy BSDF'].inputs[1].default_value = 0

    links.new(shader.outputs[0], output.inputs[0])

    return mat

# select random faces and apply change
def random_faces(mat, ratio=0.5, expand=False):
    # enter edit mode for selected object
    mesh = bpy.context.active_object.data
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(mesh)

    # select random proportion of faces
    # can use bpy.ops.mesh.select_random(ratio=0.1), but will hinder
    # selections (multiple) where needing to track faces already selected
    for f in bm.faces:
        f.select_set(False)
        
    faces = set(bm.faces)
    chosen = 0

    while faces and (chosen / len(bm.faces)) < ratio:
        face = choice(list(faces))
        face.select_set(True)
        faces -= set([face])
        chosen += 1
        
    # do stuff to selected faces...
    if expand:
        bpy.ops.mesh.select_more()
    ix = [i for i, m in enumerate(bpy.context.object.material_slots) if m.name == mat.name]
    bpy.context.object.active_material_index = ix[0]
    bpy.ops.object.material_slot_assign()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
# assign emission material to the object
mat = newShader('lights', 'emission', 1, 1, 1)
bpy.context.active_object.data.materials.append(mat)
random_faces(mat, ratio=0.02, expand=True)