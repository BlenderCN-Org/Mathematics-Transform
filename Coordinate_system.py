import bpy
import mathutils
import math
from bpy.props import *
       
ob_location = bpy.context.object.location
ob_t1 = math.degrees(math.atan(math.sqrt(math.pow(ob_location.x,2)+math.pow(ob_location.y,2))/ob_location.z))
ob_t2 = math.degrees(math.atan2(ob_location.y,ob_location.x))
    
def sphere_update(self, context):
    r = context.object.mysphere_radius
    t1 = math.radians(context.object.mysphere_t1)
    t2 = math.radians(context.object.mysphere_t2)
    x = r*math.sin(t1)*math.cos(t2)
    y = r*math.sin(t1)*math.sin(t2)
    z = r*math.cos(t1)
    context.object.location.x = x
    context.object.location.y = y
    context.object.location.z = z

def test1(self, context):
    r = bpy.context.object.location.length
    t1= math.degrees(math.atan(math.sqrt(math.pow(ob_location.x,2)+math.pow(ob_location.y,2))/ob_location.z))
    t2 = math.degrees(math.atan2(ob_location.y,ob_location.x))
    bpy.types.Object.mysphere_radius = r
    bpy.types.Object.mysphere_t1 = t1
    bpy.types.Object.mysphere_t2 = t2

bpy.types.Object.mysphere_radius = FloatProperty(
    name = "r", 
    default = bpy.context.object.location.length,
    update = sphere_update)

bpy.types.Object.mysphere_t1 = FloatProperty(
    name = "θ", 
    default = ob_t1, min = 0, max = 360,
    update = sphere_update)

bpy.types.Object.mysphere_t2 = FloatProperty(
    name = "φ", 
    default = ob_t2, min = 0, max = 360,
    update = sphere_update)
    
class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "myTransform"
    #bl_idname = "myTransform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_context = "scene"
    

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        active_obj = bpy.context.active_object
        
        layout.label(text = "sphere coordinate")
        row = layout.row()
        row.column().prop(active_obj, "mysphere_radius")
        layout.column().prop(active_obj, "mysphere_t1")
        layout.column().prop(active_obj, "mysphere_t2")

def register():
    bpy.utils.register_class(LayoutDemoPanel)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
    register()