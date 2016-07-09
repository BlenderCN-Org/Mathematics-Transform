import bpy
import mathutils
import math
from bpy.props import *

#更動求座標系時呼叫來更動active_object座標系之函數       
def sphere_update(self, context):
    sphere_coordinate = context.scene.sphere_coordinate
    r = sphere_coordinate.radius
    t1 = math.radians(sphere_coordinate.polar)
    t2 = math.radians(sphere_coordinate.azimuth)
    x = r*math.sin(t1)*math.cos(t2)
    y = r*math.sin(t1)*math.sin(t2)
    z = r*math.cos(t1)
    context.object.location.x = x
    context.object.location.y = y
    context.object.location.z = z
"""
期望在Position更動時跟著呼叫的函數

def test1(self, context):
    r = bpy.context.object.location.length
    t1= math.degrees(math.atan(math.sqrt(math.pow(ob_location.x,2)+math.pow(ob_location.y,2))/ob_location.z))
    t2 = math.degrees(math.atan2(ob_location.y,ob_location.x))
    bpy.types.Object.mysphere_radius = r
    bpy.types.Object.mysphere_t1 = t1
    bpy.types.Object.mysphere_t2 = t2
"""

#將放在scene下的一個PropertyGroup，用來儲存半徑、天頂角、方位角的數值
class Sphere_coordinate(bpy.types.PropertyGroup):
    radius = FloatProperty(
        name = "r", 
        default = 0,
        update = sphere_update)

    polar = FloatProperty(
        name = "θ", 
        default = 0, min = 0, max = 360,
        update = sphere_update)

    azimuth = FloatProperty(
        name = "φ", 
        default = 0, min = 0, max = 360,
        update = sphere_update)    

#在Scene底下加入Sphere_coordinate的PropertyGroup             
bpy.utils.register_class(Sphere_coordinate)
bpy.types.Scene.sphere_coordinate = bpy.props.PointerProperty(type = Sphere_coordinate)


#UI部分
class Coodinate_system(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Coordinate System"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    

    def draw(self, context):
        layout = self.layout

        Sphere_coordinate = context.scene.sphere_coordinate
        
        layout.label(text = "sphere coordinate")
        row = layout.row()
        row.column().prop(Sphere_coordinate, "radius")
        layout.column().prop(Sphere_coordinate, "polar")
        layout.column().prop(Sphere_coordinate, "azimuth")

def register():
    bpy.utils.register_class(Coodinate_system)


def unregister():
    bpy.utils.unregister_class(Coodinate_system)


if __name__ == "__main__":
    register()