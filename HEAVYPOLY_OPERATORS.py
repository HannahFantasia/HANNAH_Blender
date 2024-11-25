import bpy

class HP_OT_SmartScale(bpy.types.Operator):
    bl_idname = "view3d.smart_scale"        # unique identifier for buttons and menu items to reference.
    bl_label = "Context Sensitive Scale"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    

    def invoke(self, context, event):
        modal = False
        try:
            for ob in bpy.context.selected_objects:
                if ob.mode == 'OBJECT' and ob.children == () and ob.data.users == 1 and ob.type == 'MESH':
                    modal = True
                    print('running modal')
        except:
            pass

        if modal:
            context.window_manager.modal_handler_add(self)
            print('Scaling MODAL')

        bpy.ops.transform.resize('INVOKE_DEFAULT', mirror=True)
        return {'RUNNING_MODAL'}


    def modal(self, context, event):
        print("MODAL " + event.type)
        if event.type == 'MOUSEMOVE':
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        else:
            return {'RUNNING_MODAL'}

class HP_OT_SeparateAndSelect(bpy.types.Operator):
    bl_idname = "object.separate_and_select"        # unique identifier for buttons and menu items to reference.
    bl_label = "Separate and Select"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.


    @classmethod
    def poll(cls, context):
        return (context.selected_objects is not None and 
                bpy.context.object.type in {'MESH', 'GREASEPENCIL', 'ARMATURE', 'CURVE', 'SURFACE'})


    def execute(self, context):
        self.separate_and_select(context)
        return {'FINISHED'}


    def separate_and_select(self, context):
        bases = bpy.context.selected_objects
        obj_type = bpy.context.object.type
        
        # Handle the separation logic for different object types
        match obj_type:
            case 'MESH':
                bpy.ops.mesh.separate(type='SELECTED')
            case 'GREASEPENCIL':
                bpy.ops.grease_pencil.separate(mode='SELECTED')
            case 'ARMATURE':
                bpy.ops.armature.separate() 
            case 'CURVE':
                bpy.ops.curve.separate()
            case 'SURFACE':
                bpy.ops.curve.separate()
            case _:
                print(f"Unsupported type: {obj_type}")
        

        bpy.ops.object.mode_set(mode='OBJECT')
        selected = bpy.context.selected_objects

        bpy.context.view_layer.objects.active = selected[-1] # separated object
        new_object = bpy.context.view_layer.objects.active

        bpy.ops.object.select_all(action='DESELECT')
        new_object.select_set(True)

        bpy.context.view_layer.objects.active = new_object
        

class HP_OT_SmartShadeSmooth(bpy.types.Operator):
    bl_idname = "view3d.smart_shade_smooth_toggle"        # unique identifier for buttons and menu items to reference.
    bl_label = "Smart Shade Smooth"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.


    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None


    def execute(self, context):
        self.smart_shade_smooth(context)
        return {'FINISHED'}


    def smart_shade_smooth(self, context):
        isedit = False
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH':
                if ob.mode == 'EDIT':
                    isedit = True
                    bpy.ops.object.editmode_toggle()
                bpy.ops.object.shade_auto_smooth(use_auto_smooth=True, angle=0.436332) 
                if isedit:
                    bpy.ops.object.editmode_toggle()

class HP_OT_Subdivision_Toggle(bpy.types.Operator):
    bl_idname = "view3d.subdivision_toggle"
    bl_label = "Subdivision Toggle"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None


    def execute(self, context):
        self.toggle_subdivision(context)
        return {'FINISHED'}


    def toggle_subdivision(self, context):
        for o in context.selected_objects:
            context.view_layer.objects.active = o
            if 0 < len([m for m in context.object.modifiers if m.type == "SUBSURF"]):
                if  context.object.modifiers["Subsurf_Base"].show_viewport == False:
                    context.object.modifiers["Subsurf_Base"].show_render = True
                    context.object.modifiers["Subsurf_Base"].show_viewport = True
                else:
                    context.object.modifiers["Subsurf_Base"].show_render = False
                    context.object.modifiers["Subsurf_Base"].show_viewport = False
            else:
                mod = o.modifiers.new("Subsurf_Base", "SUBSURF")
                mod.name = "Subsurf_Base"
                mod.render_levels = 3
                mod.levels = 3
                mod.show_in_editmode = True
                mod.show_on_cage = False
                mod.subdivision_type = 'CATMULL_CLARK'


def menu_func(self, context):
    self.layout.operator(HP_OT_Subdivision_Toggle.bl_idname, text=HP_OT_Subdivision_Toggle.bl_label)
    self.layout.operator(HP_OT_SmartShadeSmooth.bl_idname, text=HP_OT_SmartShadeSmooth.bl_label)
    self.layout.operator(HP_OT_SeparateAndSelect.bl_idname, text=HP_OT_SeparateAndSelect.bl_label)
    self.layout.operator(HP_OT_SmartScale.bl_idname, text=HP_OT_SmartScale.bl_label)


classes = (
    HP_OT_Subdivision_Toggle,
    HP_OT_SmartShadeSmooth,
    HP_OT_SeparateAndSelect,
    HP_OT_SmartScale,
)