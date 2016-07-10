import bpy
import mathutils
import math
from bpy.props import *

#更動求座標系時呼叫來更動active_object座標系之函數       
def update_Cartesian(self, context):
    Sphere_Coordinate = context.scene.Sphere_Coordinate
    r = Sphere_Coordinate.radius
    polar = math.radians(Sphere_Coordinate.polar)
    azimuth = math.radians(Sphere_Coordinate.azimuth)
    x = r*math.sin(polar)*math.cos(azimuth)
    y = r*math.sin(polar)*math.sin(azimuth)
    z = r*math.cos(polar)
    context.object.location.x = x
    context.object.location.y = y
    context.object.location.z = z
    
#預期用來修改球座標系的函數
def update_Sphere(self, context):
    ob = bpy.context.scene.Cartesian_coordinate
    radius = ob.length
    polar= math.degrees(math.acos(ob.z/radius))
    azimuth = math.degrees(math.atan2(ob.y,ob.x))
    Sphere_Coordinate = context.scene.Sphere_Coordinate
    Sphere_Coordinate.radius = radius
    Sphere_Coordinate.polar = polar
    Sphere_Coordinate.azimuth = azimuth


#Cartesian coordinate
#將放在scene下的一個PropertyGroup，用來儲存半徑、天頂角、方位角的數值
class Sphere_Coordinate(bpy.types.PropertyGroup):
    radius = FloatProperty(
        name = "r", 
        default = 0, min = 0,
        update = update_Cartesian)

    polar = FloatProperty(
        name = "θ", 
        default = 0, min = 0, max = 180,
        update = update_Cartesian)

    azimuth = FloatProperty(
        name = "φ", 
        default = 0, min = -180, max = 180,
        update = update_Cartesian)
    
#在Scene底下加入Sphere_coordinate的PropertyGroup         
       
bpy.utils.register_class(Sphere_Coordinate)
bpy.types.Scene.Sphere_Coordinate = bpy.props.PointerProperty(type = Sphere_Coordinate)
bpy.types.Scene.Cartesian_Coordinate = FloatVectorProperty(subtype = 'TRANSLATION',update = update_Sphere)

#UI部分
class Coodinate_system_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Coordinate System"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        Sphere_Coordinate = context.scene.Sphere_Coordinate

        layout.label(text = "Sphere Coordinate")
        row = layout.row()
        row.column().prop(Sphere_Coordinate, "radius")
        layout.column().prop(Sphere_Coordinate, "polar")
        layout.column().prop(Sphere_Coordinate, "azimuth")
            
def register():
    
    bpy.utils.register_class(Coodinate_system_Panel)

def unregister():
    bpy.utils.unregister_class(Coodinate_system_Panel)

if __name__ == "__main__":
    register()