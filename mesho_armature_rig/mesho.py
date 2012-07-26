import bpy
from bpy_extras import object_utils

"""
Blender 2.61

Alt + P en esta ventana
con la armadura seleccionada
para crear el MESH

Alt + A en la vista 3D
para ver el resultado

"""

def main():
    
    diferencia = 0
    multiplicador = 0.8
    
    armature = bpy.context.active_object
    
    try:
        if armature.type!='ARMATURE':
            return
    except:
        return
    
    
    bones = armature.data.bones
    
    #AGREGAR UN OBJETO MESH
    
    context = bpy.context
    mesh = bpy.data.meshes.new('mesho')          # create a new mesh
    #ob = bpy.data.objects.new(mesh.name,mesh)
    object_utils.object_data_add(context, mesh, operator=None)
    ob = bpy.data.objects[mesh.name]
    
    
    verts = []
    edges = []
    
    for i in bones:
        
        try:
            index_head = verts.index(i.head_local)
        except:
            verts.append(i.head_local)
            index_head = verts.index(i.head_local)
            
        try:
            index_tail = verts.index(i.tail_local)
        except:
            verts.append(i.tail_local)
            index_tail = verts.index(i.tail_local)
            
        

        edges.append((index_head,index_tail))
        
        
             
    mesh.from_pydata(verts,edges,[])
    
    ob.vertex_groups.new("PESOS")
    
    for i in bones:

        #AGREGA VERTICE A UN GRUPO CON SU INDICE
        index_tail = verts.index(i.tail_local)
        
        peso = 1*pow(multiplicador,len(i.parent_recursive))-diferencia*len(i.parent_recursive)
        
        ob.vertex_groups.new(i.name)           
        ob.vertex_groups[i.name].add([index_tail],1,'ADD')
        
        ob.vertex_groups["PESOS"].add([index_tail],peso,'ADD')
        
        #print(index_tail,ob.vertex_groups[i.name])
   
        try:
            trackto = armature.pose.bones[i.name].constraints["Stretch To"]
            armature.pose.bones[i.name].constraints.remove(trackto)
        except:
            pass  
          
        armature.pose.bones[i.name].constraints.new("STRETCH_TO")
        trackto = armature.pose.bones[i.name].constraints["Stretch To"]
        
        
        trackto.target = ob
        trackto.subtarget = i.name
        
        ob.modifiers.new("Soft Body","SOFT_BODY")
        softbody = ob.modifiers["Soft Body"]
        softbody.settings.vertex_group_goal="PESOS"
        softbody.settings.goal_default=1


main()




