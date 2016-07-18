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
import bgl
import blf

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
            if updated_variable == self.update_request:
                self.update_request = True
    def update(self):
        if self.update_request:
            Mathematics_Coordinates_System = bpy.context.scene.Mathematics_Coordinates_System
            Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
            ob = bpy.context.scene.objects.active.location
            x = ob.x
            y = ob.y
            z = ob.z
            Sph_r = Coordinate_variable.Sphere_radius
            Sph_t1 = math.radians(Coordinate_variable.Sphere_polar)
            Cy_r = Coordinate_variable.Cylindrical_radius
            t2 = math.radians(Coordinate_variable.azimuth)
            
            if self.updated_Prop == "Cartesian_Coordinate_variable":
                self.update_Cylindrical()
                self.update_Sphere()
            elif self.updated_Prop == "Cylindrical_radius":
                Coordinate_variable.Sphere_radius = math.sqrt(math.pow(z,2)+math.pow(Cy_r,2))
                if z !=0 :
                    Coordinate_variable.Sphere_polar = math.degrees(math.atan2(Cy_r,z))
                self.update_Cartesian("Cylindrical_radius")
            elif self.updated_Prop == "Sphere_polar":
                Coordinate_variable.Cylindrical_radius = Sph_r*math.sin(Sph_t1)
                ob.z = Sph_r*math.cos(Sph_t1)
                self.update_Cartesian("Sphere_polar")
            elif self.updated_Prop == "Sphere_radius":
                Coordinate_variable.Cylindrical_radius = Sph_r*math.sin(Sph_t1)
                ob.z = Sph_r*math.cos(Sph_t1)
                self.update_Cartesian("Sphere_radius")
            elif self.updated_Prop == "azimuth":
                ob.x = Cy_r*math.cos(t2)
                ob.y = Cy_r*math.sin(t2)
            self.update_request = False
        else:
            self.updated_Prop = None
    def update_Cartesian(self,variable):
        ob = bpy.context.scene.objects.active.location
        Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
        Sph_r = Coordinate_variable.Sphere_radius
        Sph_t1 = math.radians(Coordinate_variable.Sphere_polar)
        Cy_r = Coordinate_variable.Cylindrical_radius
        t2 = math.radians(Coordinate_variable.azimuth)
        
        if (variable == "Sphere_radius")|(variable == "Sphere_polar"):
            ob.x = Sph_r*math.sin(Sph_t1)*math.cos(t2)
            ob.y = Sph_r*math.sin(Sph_t1)*math.sin(t2)
            ob.z = Sph_r*math.cos(Sph_t1)
        elif variable == "Cylindrical_radius":
            ob.x = Cy_r*math.cos(t2)
            ob.y = Cy_r*math.sin(t2)

    def update_Sphere(self):
        ob = bpy.context.scene.objects.active.location
        Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
        x = ob.x
        y = ob.y
        z = ob.z
        Shp_r = ob.length
        
        if x == 0:
            if y >= 0:
                Coordinate_variable.azimuth = 90  
            else:
                Coordinate_variable.azimuth = -90          
        else:
            Coordinate_variable.azimuth = math.degrees(math.atan2(y,x))
        Coordinate_variable.Sphere_radius = Shp_r
        if Shp_r != 0:
            t = z/Shp_r
            if t >= 1:
                Coordinate_variable.Sphere_polar =0
            elif t <= -1:
                Coordinate_variable.Sphere_polar =180
            else:
                Coordinate_variable.Sphere_polar = math.degrees(math.acos(t))

    def update_Cylindrical(self):
        ob = bpy.context.scene.objects.active.location
        Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
        x = ob.x
        y = ob.y
        
        Coordinate_variable.Cylindrical_radius = math.sqrt(math.pow(y,2)+math.pow(x,2))
        if x == 0:
            if y >= 0:
                Coordinate_variable.azimuth = 90  
            else:
                Coordinate_variable.azimuth = -90          
        else:
            Coordinate_variable.azimuth = math.degrees(math.atan2(y,x))
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
        Coordinate_variable = scene.Mathematics_Coordinates_System.Coordinate_variable
        ob = bpy.context.scene.objects.active
        
        layout.column().prop(scene.Mathematics_Coordinates_System,"Chosen_Coordinate",text = "")
        if scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Sphere_Coordinate":
            col = layout.column()
            col.prop(Coordinate_variable, "Sphere_radius")
            col.prop(Coordinate_variable, "Sphere_polar")
            col.prop(Coordinate_variable, "azimuth")
        elif scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Cylindrical_Coordinate":
            col = layout.column()
            col.prop(Coordinate_variable, "Cylindrical_radius")
            col.prop(Coordinate_variable, "azimuth")
            col.prop(ob, "location", index = 2, text = "z")
        elif scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Cartesian_Coordinate":
            col = layout.column()
            col.prop(bpy.context.scene.objects.active, "location", text = "")
            
        if Mathematics_Transform_Reference.is_enabled:
            layout.operator("view3d.mathematics_transform_reference", "Stop", icon="PAUSE")
        else:
            layout.operator("view3d.mathematics_transform_reference", "Start", icon="PLAY")

def frange(start, stop, step):
 i = start
 while i < stop:
    yield i
    i += step

class Mathematics_Transform_Reference(bpy.types.Operator):
    bl_idname = "view3d.mathematics_transform_reference"
    bl_label = "Mathematics_Transform_Reference"

    _handle_draw = None
    is_enabled = False
    
    

    def draw_Cartesian(self):#vertices):
        ob = bpy.context.scene.objects.active.location
        #bgl.glClear()
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glLineWidth(4)    
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex3f(0,0,0)
        bgl.glColor4f(100, 0.0, 0.0, 1)
        bgl.glVertex3f(ob.x,0,0)
        bgl.glColor4f(0, 100.0, 0.0, 1)
        bgl.glVertex3f(ob.x,ob.y,0)
        bgl.glColor4f(0, 0.0, 100.0, 1)
        bgl.glVertex3f(ob.x,ob.y,ob.z)
        bgl.glEnd()
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        #bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

    def draw_Sphere(self):#vertices):
        ob = bpy.context.scene.objects.active.location
        Mathematics_Coordinates_System = bpy.context.scene.Mathematics_Coordinates_System
        Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
        Sph_r = Coordinate_variable.Sphere_radius
        Sph_t1 = math.radians(Coordinate_variable.Sphere_polar)
        Cy_r = Coordinate_variable.Cylindrical_radius
        t2 = math.radians(Coordinate_variable.azimuth)
        
        #bgl.glClear()
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glLineWidth(4)    
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex3f(0,0,0)
        bgl.glColor4f(0, 0, 1, 1)
        bgl.glVertex3f(0,0,Sph_r)
        bgl.glColor4f(0, 1, 1, 1)

        
        a = Sph_t1
        b = math.pi/(300*Sph_r)
        for t in frange(0,a,b):
            
            x = Sph_r*math.sin(t)
            y = 0
            z = Sph_r*math.cos(t)
            bgl.glVertex3f(x,y,z)
        
        bgl.glColor4f(1, 0, 1, 1)
        
        if t2 >= 0 :
            c = t2
        else:
            c  = -t2
        
        d = math.pi/(300*Sph_r)
        for t in frange(0,c+d,d):
            if(t2 >= 0):
                x = Sph_r*math.sin(a)*math.cos(t)
                y = Sph_r*math.sin(a)*math.sin(t)
            else:
                x = Sph_r*math.sin(a)*math.cos(-t)
                y = Sph_r*math.sin(a)*math.sin(-t)
            z = Sph_r*math.cos(a)
            bgl.glVertex3f(x,y,z)
            
        bgl.glEnd()
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        #bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

    def draw_Cylindrical(self):#vertices):
        ob = bpy.context.scene.objects.active.location
        Mathematics_Coordinates_System = bpy.context.scene.Mathematics_Coordinates_System
        Coordinate_variable = bpy.context.scene.Mathematics_Coordinates_System.Coordinate_variable
        Sph_r = Coordinate_variable.Sphere_radius
        Sph_t1 = math.radians(Coordinate_variable.Sphere_polar)
        Cy_r = Coordinate_variable.Cylindrical_radius
        t2 = math.radians(Coordinate_variable.azimuth)
        #bgl.glClear()
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glLineWidth(4)    
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex3f(0,0,0)
        bgl.glColor4f(1, 0.0, 0, 1)
        bgl.glVertex3f(Cy_r,0,0)
        bgl.glColor4f(1, 0, 1, 1)
        if t2 >= 0 :
            a = t2
        else:
            a = -t2
        b = math.pi/(300*Cy_r)
        for t in frange(0,a,b):
            
            if(t2 >= 0):
                x = Cy_r*math.cos(t)
                y = Cy_r*math.sin(t)
            else:
                x = Cy_r*math.cos(-t)
                y = Cy_r*math.sin(-t)
            z = 0
            bgl.glVertex3f(x,y,z)
        bgl.glColor4f(0, 0.0, 1, 1)
        #bgl.glVertex3f(ob.x,ob.y,ob.z)
        bgl.glVertex3f(ob.x,ob.y,ob.z)
        bgl.glEnd()
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        #bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    @staticmethod
    def draw_callback_px(self, context):
        scene = bpy.context.scene
        if scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Sphere_Coordinate":
            self.draw_Sphere()
        elif scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Cylindrical_Coordinate":
            self.draw_Cylindrical()
        elif scene.Mathematics_Coordinates_System.Chosen_Coordinate == "Cartesian_Coordinate":
            self.draw_Cartesian()
            

    @staticmethod
    def handle_add(self, context):
        Mathematics_Transform_Reference._handle_draw = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_callback_px, (self, context), 'WINDOW', 'POST_VIEW')

    @staticmethod
    def handle_remove():
        if Mathematics_Transform_Reference._handle_draw is not None:
            bpy.types.SpaceView3D.draw_handler_remove(Mathematics_Transform_Reference._handle_draw, 'WINDOW')
            Mathematics_Transform_Reference._handle_draw = None
            Mathematics_Transform_Reference.is_enabled = False

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            if Mathematics_Transform_Reference.is_enabled:
                self.cancel(context)
                return {'FINISHED'}
            else:
                Mathematics_Transform_Reference.handle_add(self, context)
                Mathematics_Transform_Reference.is_enabled = True

                context.area.tag_redraw()
                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def cancel(self, context):
        Mathematics_Transform_Reference.handle_remove()       
            
def register():
    bpy.app.handlers.scene_update_post.append(scene_update)
    bpy.utils.register_class(Mathematics_Transform_Reference)
    bpy.utils.register_class(Coordinate_variable)
    bpy.utils.register_class(Mathematics_Coordinates_System)
    bpy.types.Scene.Mathematics_Coordinates_System = bpy.props.PointerProperty(type = Mathematics_Coordinates_System)
    bpy.utils.register_class(Mathematics_Transform_Panel)
def unregister():
    bpy.app.handlers.scene_update_post.remove(scene_update)
    del bpy.types.Scene.Mathematics_Coordinates_System
    bpy.utils.unregister_class(Coordinate_variable)
    bpy.utils.unregister_class(Mathematics_Coordinates_System)
    bpy.utils.unregister_class(Mathematics_Transform_Reference)
    bpy.utils.unregister_class(Mathematics_Transform_Panel)
if __name__ == "__main__":
    register()