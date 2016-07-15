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
from bpy.app.handlers import persistent

#使用的座標系以及，在不同座標系下所使用的變量
Coordinates_items = [("None","None","None"),
    ("Sphere_Coordinate","Sphere_Coordinate","Sphere_Coordinate"),
    ("Cylindrical_Coordinate","Cylindrical_Coordinate","Cylindrical_Coordinate"),
    ("Cartesian_Coordinate","Cartesian_Coordinate","Cartesian_Coordinate")]
Coordinates_variables_items = [("Sphere_radius","Sphere_radius","Sphere_radius"),
    ("Cylindrical_radius","Cylindrical_radius","Cylindrical_radius"),
    ("Sphere_polar","Sphere_polar","Sphere_polar"),
    ("azimuth","azimuth","azimuth"),
    ("Cartesian_Coordinate_variable","Cartesian_Coordinate_variable","Cartesian_Coordinate_variable")]
    
#更新座標系---------------------------------------
@persistent
def scene_update(context):
    if bpy.context.scene.objects.active.is_updated: 
        Coordinate_Property_update("Cartesian_Coordinate_variable")
    Coordinate_Property_update.update()

#用來管理座標間的更新
class Coordinate_updater():
    def __init__(self):
        self.update_request = False
        self.updated_Prop = None
    def __call__(self,updated_variable):
        if not self.updated_Prop:
            self.updated_Prop = updated_variable    
            self.update_request = True
        self.update_request = True
    def update(self):
        if self.update_request:
            Mathematics_Coordinates_System = bpy.context.scene.Mathematics_Coordinates_System
            Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
            ob = bpy.context.scene.objects.active.location
            if self.updated_Prop == "Cartesian_Coordinate_variable":
                self.update_Cylindrical()
                self.update_Sphere()
            elif self.updated_Prop == "Cylindrical_radius":
                Coordinate_variable.Sphere_radius = math.sqrt(math.pow(ob.z,2)+math.pow(Coordinate_variable.Cylindrical_radius,2))
                if ob.z !=0 :
                    Coordinate_variable.Sphere_polar = math.degrees(math.atan2(Coordinate_variable.Cylindrical_radius,ob.z))
                self.update_Cartesian("Cylindrical_radius")
            elif self.updated_Prop == "Sphere_polar":
                Coordinate_variable.Cylindrical_radius = Coordinate_variable.Sphere_radius*math.sin(math.radians(Coordinate_variable.Sphere_polar))
                ob.z = Coordinate_variable.Sphere_radius*math.cos(math.radians(Coordinate_variable.Sphere_polar))
                self.update_Cartesian("Sphere_polar")
            elif self.updated_Prop == "Sphere_radius":
                Coordinate_variable.Cylindrical_radius = Coordinate_variable.Sphere_radius*math.sin(math.radians(Coordinate_variable.Sphere_polar))
                ob.z = Coordinate_variable.Sphere_radius*math.cos(math.radians(Coordinate_variable.Sphere_polar))
                self.update_Cartesian("Sphere_radius")
            elif self.updated_Prop == "azimuth":
                ob = bpy.context.scene.objects.active.location
                Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
                ob.x = Coordinate_variable.Cylindrical_radius*math.cos(math.radians(Coordinate_variable.azimuth))
                ob.y = Coordinate_variable.Cylindrical_radius*math.sin(math.radians(Coordinate_variable.azimuth))
            self.update_request = False
        else:
            self.updated_Prop = None
    def update_Cartesian(self,variable):
        if (variable == "Sphere_radius")|(variable == "Sphere_polar"):
            Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
            r = Coordinate_variable.Sphere_radius
            x = r*math.sin(math.radians(Coordinate_variable.Sphere_polar))*math.cos(math.radians(Coordinate_variable.azimuth))
            y = r*math.sin(math.radians(Coordinate_variable.Sphere_polar))*math.sin(math.radians(Coordinate_variable.azimuth))
            z = r*math.cos(math.radians(Coordinate_variable.Sphere_polar))
            bpy.context.scene.objects.active.location.x = x
            bpy.context.scene.objects.active.location.y = y
            bpy.context.scene.objects.active.location.z = z
        elif variable == "Cylindrical_radius":
            Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
            r = Coordinate_variable.Cylindrical_radius
            bpy.context.scene.objects.active.location.x = r*math.cos(math.radians(Coordinate_variable.azimuth))
            bpy.context.scene.objects.active.location.y = r*math.sin(math.radians(Coordinate_variable.azimuth))

    def update_Sphere(self):
        ob = bpy.context.scene.objects.active.location
        Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
        Sphere_radius = ob.length
        if ob.x == 0:
            if ob.y >= 0:
                Coordinate_variable.azimuth = 90  
            else:
                Coordinate_variable.azimuth = -90          
        else:
            Coordinate_variable.azimuth = math.degrees(math.atan2(ob.y,ob.x))
        Coordinate_variable.Sphere_radius = Sphere_radius
        if Sphere_radius != 0:
            t = ob.z/Sphere_radius
            if t >= 1:
                Sphere_radius = ob.z
                Coordinate_variable.Sphere_polar =0
            elif t <= -1:
                Sphere_radius = ob.z
                Coordinate_variable.Sphere_polar =180
            else:
                Coordinate_variable.Sphere_polar = math.degrees(math.acos(t))

    def update_Cylindrical(self):
        ob = bpy.context.scene.objects.active.location
        Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
        Coordinate_variable.Cylindrical_radius = math.sqrt(math.pow(ob.y,2)+math.pow(ob.x,2))
        if ob.x == 0:
            if ob.y >= 0:
                Coordinate_variable.azimuth = 90  
            else:
                Coordinate_variable.azimuth = -90          
        else:
            Coordinate_variable.azimuth = math.degrees(math.atan2(ob.y,ob.x))
Coordinate_Property_update = Coordinate_updater()

#在scene底下存放座標變量的PropertyGroup
class Coordinate_variable(bpy.types.PropertyGroup):
        Sphere_radius = FloatProperty(
            name = "r", precision = 5,
            default = 0, min = 0,
            update = lambda self,context : Coordinate_Property_update("Sphere_radius"))
        Cylindrical_radius = FloatProperty(
            name = "r", precision = 5,
            default = 0, min = 0,
            update = lambda self,context : Coordinate_Property_update("Cylindrical_radius"))
        Sphere_polar = FloatProperty(
            name = "θ", precision = 5,
            default = 0, min = 0, max = 180,
            update = lambda self,context : Coordinate_Property_update("Sphere_polar"))
        azimuth = FloatProperty(
            name = "φ", precision = 5,
            default = 0, min = -180, max = 180,
            update = lambda self,context : Coordinate_Property_update("azimuth"))

#數學座標系統的類別
class Mathematics_Coordinates_System(bpy.types.PropertyGroup):
    Chosen_Coordinate = EnumProperty(items = Coordinates_items, default = "None")
    updated_variable = EnumProperty(items = Coordinates_variables_items, default = None )
    Coordinate_variable = bpy.props.PointerProperty(type = Coordinate_variable)
    
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
            col = layout.column()
            col.prop(scene.Mathematics_Coordinates_System.Coordinate_variable, "Sphere_radius")
            col.prop(scene.Mathematics_Coordinates_System.Coordinate_variable, "Sphere_polar")
            col.prop(scene.Mathematics_Coordinates_System.Coordinate_variable, "azimuth")
        elif scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Cylindrical_Coordinate":
            col = layout.column()
            col.prop(scene.Mathematics_Coordinates_System.Coordinate_variable, "Cylindrical_radius")
            col.prop(scene.Mathematics_Coordinates_System.Coordinate_variable, "azimuth")
            col.prop(bpy.context.scene.objects.active, "location", index = 2, text = "z")
        elif scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Cartesian_Coordinate":
            col = layout.column()
            col.prop(bpy.context.scene.objects.active, "location", text = "")
            
            
def register():
    bpy.app.handlers.scene_update_post.append(scene_update)
    bpy.utils.register_class(Coordinate_variable)
    bpy.utils.register_class(Mathematics_Coordinates_System)
    bpy.types.Scene.Mathematics_Coordinates_System = bpy.props.PointerProperty(type = Mathematics_Coordinates_System)
    bpy.utils.register_class(Mathematics_Transform_Panel)
def unregister():
    bpy.app.handlers.scene_update_post.remove(scene_update)
    del bpy.types.Scene.Mathematics_Coordinates_System
    bpy.utils.unregister_class(Coordinate_variable)
    bpy.utils.unregister_class(Mathematics_Coordinates_System)
    bpy.utils.unregister_class(Mathematics_Transform_Panel)
if __name__ == "__main__":
    register()