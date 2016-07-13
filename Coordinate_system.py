import bpy
import mathutils
import math
from bpy.props import *

#更動求座標系時呼叫來更動active_object座標系之函數       
def update_Cartesian(self, context):
    if(self.__class__.__name__ == 'Sphere_Coordinate'):
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
        
    if(self.__class__.__name__ == 'Cylindrical_Coordinate'):
        Cylindrical_Coordinate = context.scene.Cylindrical_Coordinate
        r = Cylindrical_Coordinate.radius
        azimuth = math.radians(Cylindrical_Coordinate.azimuth)
        x = r*math.cos(azimuth)
        y = r*math.sin(azimuth)
        context.object.location.x = x
        context.object.location.y = y
        context.object.location.z = Cylindrical_Coordinate.height
    
#預期用來修改球座標系的函數
def update_Sphere(context):
    ob = bpy.context.object.location
    radius = ob.length
    polar= math.degrees(math.acos(ob.z/radius))
    azimuth = math.degrees(math.atan2(ob.y,ob.x))
    Sphere_Coordinate = bpy.context.scene.Sphere_Coordinate
    Sphere_Coordinate.radius = radius
    Sphere_Coordinate.polar = polar
    Sphere_Coordinate.azimuth = azimuth
    
def update_Cylindrical(context):
    ob = bpy.context.object.location
    Cylindrical_Coordinate = bpy.context.scene.Cylindrical_Coordinate
    Cylindrical_Coordinate.radius = math.sqrt(math.pow(ob.y,2)+math.pow(ob.x,2))
    Cylindrical_Coordinate.azimuth = math.degrees(math.atan2(ob.y,ob.x))
    Cylindrical_Coordinate.height = ob.z
    
Coordinates_Dic = {'Cartesian_Coordinate':update_Cartesian,
    'Sphere_Coordinate':update_Sphere, 
    'Cylindrical_Coordinate':update_Cylindrical}
    
def scene_update(context):
    if bpy.context.active_object.is_updated:
        #update_Cylindrical(context)
        update_Sphere(context)
        update_Cylindrical(context)
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
        
class Cylindrical_Coordinate(bpy.types.PropertyGroup):
    radius = FloatProperty(
        name = "r", 
        default = 0, min = 0,
        update = update_Cartesian)
        
    azimuth = FloatProperty(
        name = "φ", 
        default = 0, min = -180, max = 180,
        update = update_Cartesian)
    
    height = FloatProperty(
        name = "z", 
        default = 0,
        update = update_Cartesian)

#UI部分
class Coodinate_system_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Coordinate System"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene

        layout.label(text = "Sphere Coordinate")
        row = layout.row()
        row.column().prop(scene.Sphere_Coordinate, "radius")
        layout.column().prop(scene.Sphere_Coordinate, "polar")
        layout.column().prop(scene.Sphere_Coordinate, "azimuth")
        
        layout.label(text = "Cylindrical Coordinate")
        row = layout.row()
        row.column().prop(scene.Cylindrical_Coordinate, "radius")
        layout.column().prop(scene.Cylindrical_Coordinate, "azimuth")
        layout.column().prop(scene.Cylindrical_Coordinate, "height")
            
def register():
    
    #在Scene底下加入Sphere_coordinate的PropertyGroup                
    bpy.utils.register_class(Sphere_Coordinate)
    bpy.types.Scene.Sphere_Coordinate = bpy.props.PointerProperty(type = Sphere_Coordinate)
    bpy.utils.register_class(Cylindrical_Coordinate)
    bpy.types.Scene.Cylindrical_Coordinate = bpy.props.PointerProperty(type = Cylindrical_Coordinate)
    #append scene_update
    bpy.app.handlers.scene_update_post.append(scene_update)
    bpy.utils.register_class(Coodinate_system_Panel)
    
def unregister():
    
    bpy.utils.unregister_class(Sphere_Coordinate)
    del bpy.types.Scene.Sphere_Coordinate
    #remove scene_update
    bpy.app.handlers.render_complete.remove(scene_update)
    bpy.utils.unregister_class(Coodinate_system_Panel)
    
if __name__ == "__main__":
    register()