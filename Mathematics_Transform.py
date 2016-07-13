bl_info = {
    "name": "Mathematics Transform",
    "author": "Stokes Lee",
    "version": (0, 1,2),
    "blender": (2, 70, 0),
    "location": "View 3D > Properties Shelf",
    "category": "3D View"
}
import bpy
import mathutils
import math
from bpy.props import *

Coordinates_items = [("None","None","None"),
    ("Sphere_Coordinate","Sphere_Coordinate","Sphere_Coordinate"),
    ("Cylindrical_Coordinate","Cylindrical_Coordinate","Cylindrical_Coordinate"),
    ("Cartesian_Coordinate","Cartesian_Coordinate","Cartesian_Coordinate")]

#更動求座標系時呼叫來更動active_object座標系之函數       
def update_Cartesian(coordinate, context):
    if(coordinate == 'Sphere_Coordinate'):
        Sphere_Coordinate = bpy.context.scene.Mathematics_Coordinates_System.Sphere_Coordinate
        r = Sphere_Coordinate.radius
        polar = math.radians(Sphere_Coordinate.polar)
        azimuth = math.radians(Sphere_Coordinate.azimuth)
        x = r*math.sin(polar)*math.cos(azimuth)
        y = r*math.sin(polar)*math.sin(azimuth)
        z = r*math.cos(polar)
        bpy.context.scene.objects.active.location.x = x
        bpy.context.scene.objects.active.location.y = y
        bpy.context.scene.objects.active.location.z = z
        
    if(coordinate == 'Cylindrical_Coordinate'):
        Cylindrical_Coordinate = bpy.context.scene.Mathematics_Coordinates_System.Cylindrical_Coordinate
        r = Cylindrical_Coordinate.radius
        azimuth = math.radians(Cylindrical_Coordinate.azimuth)
        x = r*math.cos(azimuth)
        y = r*math.sin(azimuth)
        bpy.context.scene.objects.active.location.x = x
        bpy.context.scene.objects.active.location.y = y
        bpy.context.scene.objects.active.location.z = Cylindrical_Coordinate.height
        
#預期用來修改球座標系的函數
def update_Sphere(context):
    ob = bpy.context.scene.objects.active.location
    radius = ob.length
    if ob.x == 0:
        if ob.y >=0:
            azimuth = 90
        else:
            azimuth = -90
    else:
        azimuth = math.degrees(math.atan2(ob.y,ob.x))
    Sphere_Coordinate = bpy.context.scene.Mathematics_Coordinates_System.Sphere_Coordinate
    Sphere_Coordinate.radius = radius
    if radius != 0:
        t = ob.z/radius
        print(t)
        if t >= 1:
            radius = ob.z
            Sphere_Coordinate.polar =0
        elif t <= -1:
            radius = ob.z
            Sphere_Coordinate.polar =180
        else:
            Sphere_Coordinate.polar = math.degrees(math.acos(t))
    Sphere_Coordinate.azimuth = azimuth
    Sphere_Coordinate.modify_by_Cartesian = True
    
def update_Cylindrical(context):
    ob = bpy.context.scene.objects.active.location
    Cylindrical_Coordinate = bpy.context.scene.Mathematics_Coordinates_System.Cylindrical_Coordinate
    Cylindrical_Coordinate.radius = math.sqrt(math.pow(ob.y,2)+math.pow(ob.x,2))
    if ob.x == 0:
        if ob.y >=0:
            azimuth = 90
        else:
            azimuth = -90
    else:
        azimuth = math.degrees(math.atan2(ob.y,ob.x))
    Cylindrical_Coordinate.azimuth = azimuth
    Cylindrical_Coordinate.height = ob.z
    Cylindrical_Coordinate.modify_by_Cartesian = True
    
def scene_update(context):
    Mathematics_Coordinates_System = bpy.context.scene.Mathematics_Coordinates_System
    if bpy.context.scene.objects.active.is_updated: 
        if Mathematics_Coordinates_System.updated_Coordinate == "None":
            Mathematics_Coordinates_System.updated_Coordinate = "Cartesian_Coordinate"
        else:
            Mathematics_Coordinates_System.updated_Coordinate = "None"
    if Mathematics_Coordinates_System.updated_Coordinate != "None":
        if Mathematics_Coordinates_System.updated_Coordinate == "Cartesian_Coordinate":
            update_Cylindrical(context)
            update_Sphere(context)
        elif Mathematics_Coordinates_System.updated_Coordinate == "Cylindrical_Coordinate":
            update_Sphere(context)
            update_Cartesian("Cylindrical_Coordinate", context)
        elif Mathematics_Coordinates_System.updated_Coordinate == "Sphere_Coordinate":
            update_Cylindrical(context)
            update_Cartesian("Sphere_Coordinate", context)
        
#將放在scene下的一個PropertyGroup，用來儲存半徑、天頂角、方位角的數值
def Coordinate_Property_update(self, context):
    Mathematics_Coordinates_System = bpy.context.scene.Mathematics_Coordinates_System
    if Mathematics_Coordinates_System.updated_Coordinate == "None":
        Mathematics_Coordinates_System.updated_Coordinate = self.__class__.__name__
    else:
        Mathematics_Coordinates_System.updated_Coordinate = "None"
    
class Sphere_Coordinate(bpy.types.PropertyGroup):
    radius = FloatProperty(
        name = "r", 
        default = 0, min = 0,
        update = Coordinate_Property_update)

    polar = FloatProperty(
        name = "θ", 
        default = 0, min = 0, max = 180,
        update = Coordinate_Property_update)

    azimuth = FloatProperty(
        name = "φ", 
        default = 0, min = -180, max = 180,
        update = Coordinate_Property_update)
        
class Cylindrical_Coordinate(bpy.types.PropertyGroup):
    radius = FloatProperty(
        name = "r", 
        default = 0, min = 0,
        update = Coordinate_Property_update)
        
    azimuth = FloatProperty(
        name = "φ", 
        default = 0, min = -180, max = 180,
        update = Coordinate_Property_update)
    
    height = FloatProperty(
        name = "z", 
        default = 0,
        update = Coordinate_Property_update)
        
class Mathematics_Coordinates_System(bpy.types.PropertyGroup):
    Chosen_Coordinate = EnumProperty(items = Coordinates_items, default = "None")
    updated_Coordinate = EnumProperty(items = Coordinates_items, default = "None" )
    Sphere_Coordinate = bpy.props.PointerProperty(type = Sphere_Coordinate)
    Cylindrical_Coordinate = bpy.props.PointerProperty(type = Cylindrical_Coordinate)  
    
#UI部分
class Mathematics_Transform_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Mathematics Transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        layout.column().prop(scene.Mathematics_Coordinates_System,"Chosen_Coordinate",text = "")
        if scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Sphere_Coordinate":
             
            #layout.label(text = "Sphere Coordinate")
            row = layout.row()
            row.column().prop(scene.Mathematics_Coordinates_System.Sphere_Coordinate, "radius")
            layout.column().prop(scene.Mathematics_Coordinates_System.Sphere_Coordinate, "polar")
            layout.column().prop(scene.Mathematics_Coordinates_System.Sphere_Coordinate, "azimuth")
        elif scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Cylindrical_Coordinate":
        
            #layout.label(text = "Cylindrical Coordinate")
            row = layout.row()
            row.column().prop(scene.Mathematics_Coordinates_System.Cylindrical_Coordinate, "radius")
            layout.column().prop(scene.Mathematics_Coordinates_System.Cylindrical_Coordinate, "azimuth")
            layout.column().prop(scene.Mathematics_Coordinates_System.Cylindrical_Coordinate, "height")
            
def register():
    
    #在Scene底下注冊座標系統
    bpy.utils.register_class(Sphere_Coordinate)
    bpy.utils.register_class(Cylindrical_Coordinate)
    bpy.utils.register_class(Mathematics_Coordinates_System)
    bpy.types.Scene.Mathematics_Coordinates_System = bpy.props.PointerProperty(type = Mathematics_Coordinates_System)

    #append scene_update
    bpy.app.handlers.scene_update_post.append(scene_update)
    bpy.utils.register_class(Mathematics_Transform_Panel)
    

def unregister():    
    del bpy.types.Scene.Mathematics_Coordinates_System
    bpy.utils.unregister_class(Sphere_Coordinate)
    bpy.utils.unregister_class(Cylindrical_Coordinate)
    bpy.utils.unregister_class(Mathematics_Coordinates_System)
    
    #remove scene_update
    bpy.app.handlers.scene_update_post.remove(scene_update)
    bpy.utils.unregister_class(Mathematics_Transform_Panel)
    
if __name__ == "__main__":
    register()