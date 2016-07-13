import bpy
import mathutils
import math
from bpy.props import *

Coordinates_items = [("None","None","None"),
    ("Sphere_Coordinate","Sphere_Coordinate","Sphere_Coordinate"),
    ("Cylindrical_Coordinate","Cylindrical_Coordinate","Cylindrical_Coordinate")]

#更動求座標系時呼叫來更動active_object座標系之函數       
def update_Cartesian(self, context):
    #print(context.scene.Mathematics_Coordinates_System.Cylindrical_Coordinate.radius)
    if(self.modify_by_Cartesian):
        self.modify_by_Cartesian = False
        print("###")
    else:
        #print("!!!")
        if(self.__class__.__name__ == 'Sphere_Coordinate'):
            print("!@@")
            Sphere_Coordinate = context.scene.Mathematics_Coordinates_System.Sphere_Coordinate
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
            print("!%%")
            Cylindrical_Coordinate = context.scene.Mathematics_Coordinates_System.Cylindrical_Coordinate
            r = Cylindrical_Coordinate.radius
            azimuth = math.radians(Cylindrical_Coordinate.azimuth)
            x = r*math.cos(azimuth)
            y = r*math.sin(azimuth)
            context.object.location.x = x
            context.object.location.y = y
            context.object.location.z = Cylindrical_Coordinate.height
        context.scene.Mathematics_Coordinates_System.Cartesian_modify_by = self.__class__.__name__
        #print(self.modify_by_Cartesian)
#預期用來修改球座標系的函數
def update_Sphere(context):
    ob = context.objects.active.location
    radius = ob.length
    if ob.x == 0:
        if ob.y >=0:
            azimuth = 90
        else:
            azimuth = -90
    else:
        azimuth = math.degrees(math.atan2(ob.y,ob.x))
    Sphere_Coordinate = context.Mathematics_Coordinates_System.Sphere_Coordinate
    Sphere_Coordinate.radius = radius
    if radius != 0:
        Sphere_Coordinate.polar = math.degrees(math.acos(ob.z/radius))
    Sphere_Coordinate.azimuth = azimuth
    Sphere_Coordinate.modify_by_Cartesian = True
    
def update_Cylindrical(context):
    ob = context.objects.active.location
    Cylindrical_Coordinate = context.Mathematics_Coordinates_System.Cylindrical_Coordinate
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
    update_Cylindrical(context)
    update_Sphere(context)
    """
    if context.objects.active.is_updated:
        
        if context.Mathematics_Coordinates_System.Cartesian_modify_by == "None": 
            update_Cylindrical(context)
            update_Sphere(context)
        elif context.Mathematics_Coordinates_System.Cartesian_modify_by == "Cylindrical_Coordinate":
            update_Sphere(context)
            context.Mathematics_Coordinates_System.Cartesian_modify_by = "None"
        elif context.Mathematics_Coordinates_System.Cartesian_modify_by == "Sphere_Coordinate":
            update_Cylindrical(context)
            context.Mathematics_Coordinates_System.Cartesian_modify_by = "None"
       """ 
#Cartesian coordinate
#將放在scene下的一個PropertyGroup，用來儲存半徑、天頂角、方位角的數值
class Sphere_Coordinate(bpy.types.PropertyGroup):
    modify_by_Cartesian = BoolProperty(name = "modify_by_Cartesian",default = False)
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
    modify_by_Cartesian = BoolProperty(name = "modify_by_Cartesian",default = False)
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
        
class Mathematics_Coordinates_System(bpy.types.PropertyGroup):
    Chosen_Coordinate = EnumProperty(items = Coordinates_items, default = "None")
    Cartesian_modify_by = EnumProperty(items = Coordinates_items, default = "None")
    Sphere_Coordinate = bpy.props.PointerProperty(type = Sphere_Coordinate)
    Cylindrical_Coordinate = bpy.props.PointerProperty(type = Cylindrical_Coordinate)
    
    
#UI部分
class Coordinate_system_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Coordinate System"
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
    
    #在Scene底下加入Sphere_coordinate的PropertyGroup                
    bpy.utils.register_class(Sphere_Coordinate)
    bpy.utils.register_class(Cylindrical_Coordinate)
    bpy.utils.register_class(Mathematics_Coordinates_System)
    bpy.types.Scene.Mathematics_Coordinates_System = bpy.props.PointerProperty(type = Mathematics_Coordinates_System)
    bpy.types.Scene.Sphere_Coordinate = bpy.props.PointerProperty(type = Sphere_Coordinate)
    bpy.types.Scene.Cylindrical_Coordinate = bpy.props.PointerProperty(type = Cylindrical_Coordinate)
    #append scene_update
    bpy.app.handlers.scene_update_post.append(scene_update)
    bpy.utils.register_class(Coordinate_system_Panel)
    

def unregister():    
    bpy.utils.unregister_class(Sphere_Coordinate)
    del bpy.types.Scene.Sphere_Coordinate
    #remove scene_update
    bpy.app.handlers.scene_update_post.remove(scene_update)
    bpy.utils.unregister_class(Coordinate_system_Panel)
    
if __name__ == "__main__":
    register()