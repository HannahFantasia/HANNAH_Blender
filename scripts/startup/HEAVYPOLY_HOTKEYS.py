bl_info = {
    'name': 'Hannah_Hotkeys',
    'description': 'Hotkeys',
    'author': 'Hannah Ümit and Sas van Gulik',
    'version': (0, 1, 0),
    'blender': (4, 0, 0),
    'location': '',
    'warning': '',
    'wiki_url': '',
    'category': 'Hotkeys'
    }

import bpy

window_manager = bpy.context.window_manager

def get_keymap_items_ctx(keymap_config: str , keymap_context: str):
    return window_manager.keyconfigs[keymap_config].keymaps[keymap_context].keymap_items

def remove_keymap(keymap_items_context, idname):
    keymap_item = keymap_items_context.get(idname)
    if keymap_item:
        keymap_items_context.remove(keymap_item)
    else:
        print(f"KeyMapItem {idname} not found")

def add_keymap_attrs(keymap_items_context, 
                     idname: str, 
                     event_type: str, 
                     value_key, 
                     any=False, 
                     shift=0, 
                     ctrl=0, 
                     alt=0, 
                     oskey=0, 
                     key_modifier='NONE', 
                     direction='ANY', 
                     repeat=False, 
                     head=False,
                     **kwargs):

    # Create the main keymap item
    keymap_added = keymap_items_context.new(
        idname,
        event_type,
        value_key,
        any=any,
        shift=shift,
        ctrl=ctrl,
        alt=alt,
        oskey=oskey,
        key_modifier=key_modifier,
        direction=direction,
        repeat=repeat,
        head=head
    )

    # Set properties for the keymap item
    for prop_key, prop_value in kwargs.items():
        if hasattr(keymap_added.properties, prop_key):
            setattr(keymap_added.properties, prop_key, prop_value)


    return keymap_added

def modify_modal_keymap(keymap_items_context,
                        add_modal_keymap: dict = None,
                        remove_modal_keymap: dict = None):

    if remove_modal_keymap:
        for item in reversed(keymap_items_context):
            property_value = item.propvalue
            key = item.type
            if property_value in remove_modal_keymap and key == remove_modal_keymap[property_value]:
                keymap_items_context.remove(item)
    
    if add_modal_keymap:
        for item in keymap_items_context:
            property_value = item.propvalue
            if property_value in add_modal_keymap:
                item.type = add_modal_keymap[property_value]




def global_keys(km):
    add_keymap_attrs(km, 'screen.userpref_show', 'TAB', 'PRESS' , ctrl=True)
    add_keymap_attrs(km, 'wm.window_fullscreen_toggle','F11','PRESS')
    add_keymap_attrs(km, 'screen.animation_play', 'PERIOD', 'PRESS')


def Keymap_Register():
# Remove keymap
    km = get_keymap_items_ctx('Blender', 'Frames')
    remove_keymap(km, 'screen.animation_play')
    
    km = get_keymap_items_ctx('Blender', 'Window')
    remove_keymap(km, 'wm.save_mainfile')
    remove_keymap(km, 'wm.save_as_mainfile')



# Map Window
    km = get_keymap_items_ctx('Blender', 'Window')
    add_keymap_attrs(km, 'transform.translate', 'SPACE', 'PRESS')
    add_keymap_attrs(km, 'wm.console_toggle', 'TAB', 'PRESS', ctrl=True, shift=True)
    add_keymap_attrs(km, 'wm.call_menu_pie','S','PRESS', ctrl=True, name='HP_MT_pie_save')
    add_keymap_attrs(km, 'wm.call_menu_pie','S','PRESS', ctrl=True, shift=True, name='HP_MT_pie_importexport')
    add_keymap_attrs(km, 'script.reload', 'U', 'PRESS', shift=True)

# Map Image
    # km = get_keymap_items_ctx('Blender', 'Image')
    # add_keymap_attrs(km, 'image.view_all', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True, fit_view=True)

# Map Node Editor
    km = get_keymap_items_ctx('Blender', 'Node Editor')
    add_keymap_attrs(km, 'node.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)


# Map Animation
    km = get_keymap_items_ctx('Blender', 'Animation')
    add_keymap_attrs(km, 'anim.change_frame', 'MIDDLEMOUSE', 'PRESS')
    
# Map Dopesheet
    km = get_keymap_items_ctx('Blender', 'Dopesheet')
    add_keymap_attrs(km, 'clip.dopesheet_view_all  ', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    add_keymap_attrs(km, 'transform.transform', 'SPACE', 'PRESS' , mode='TIME_TRANSLATE')

# Map Graph Editor
    km = get_keymap_items_ctx('Blender', 'Graph Editor')
    add_keymap_attrs(km, 'graph.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    add_keymap_attrs(km, 'graph.cursor_set', 'LEFTMOUSE', 'PRESS', alt = True)
    
# Map UV Editor
    km = get_keymap_items_ctx('Blender', 'UV Editor')
    add_keymap_attrs(km, 'image.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    
#Map 3D View
    km = get_keymap_items_ctx('Blender', '3D View')
    add_keymap_attrs(km, 'view3d.view_selected', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)
    add_keymap_attrs(km, 'view3d.render_border', 'B', 'PRESS',shift=True, ctrl=True)
    add_keymap_attrs(km, 'wm.call_menu_pie', 'SPACE','PRESS',ctrl=True, name='HP_MT_pie_select')
    add_keymap_attrs(km, 'wm.call_menu_pie', 'SPACE', 'PRESS',ctrl=True, alt=True, name='HP_MT_pie_rotate90')
    add_keymap_attrs(km, 'wm.call_menu_pie', 'V', 'PRESS', name='HP_MT_pie_view')
    add_keymap_attrs(km, 'wm.call_menu_pie','M','PRESS', alt=True, name='HP_MT_pie_symmetry')
    add_keymap_attrs(km, 'wm.call_menu_pie', 'SPACE','PRESS',ctrl=True, shift=True, name='HP_MT_pie_pivots')
    add_keymap_attrs(km, 'wm.call_menu_pie','Z','PRESS', name='HP_MT_pie_shading')
    add_keymap_attrs(km, 'wm.call_menu_pie', 'B', 'PRESS',ctrl=True, name='HP_MT_pie_boolean')
    add_keymap_attrs(km, 'view3d.subdivision_toggle','TAB','PRESS')
    
#Map Mesh
    km = get_keymap_items_ctx('Blender', 'Mesh')
    add_keymap_attrs(km, 'mesh.select_linked', 'LEFTMOUSE', 'DOUBLE_CLICK', delimit={'SEAM'})
    add_keymap_attrs(km, 'mesh.dupli_extrude_cursor','E','PRESS')
    add_keymap_attrs(km, 'wm.call_menu', 'E', 'PRESS', ctrl=True, name='VIEW3D_MT_edit_mesh_extrude')
    add_keymap_attrs(km, 'mesh.select_prev_item','TWO','PRESS')
    add_keymap_attrs(km, 'mesh.select_next_item','THREE','PRESS')
    add_keymap_attrs(km, 'mesh.select_less','TWO','PRESS', ctrl=True) 
    add_keymap_attrs(km, 'mesh.select_more','THREE','PRESS', ctrl=True)
    add_keymap_attrs(km, 'mesh.inset', 'SPACE', 'PRESS', alt=True)
    add_keymap_attrs(km, 'mesh.edgering_select', 'LEFTMOUSE', 'DOUBLE_CLICK', alt=True)
    add_keymap_attrs(km, 'mesh.edgering_select', 'LEFTMOUSE', 'DOUBLE_CLICK', ctrl=True, alt=True, toggle=True)
    add_keymap_attrs(km, 'mesh.bridge_edge_loops', 'B', 'PRESS', shift=True)
    add_keymap_attrs(km, 'mesh.bridge_edge_loops', 'B', 'PRESS', ctrl=True, shift=True, number_cuts=12)
    add_keymap_attrs(km, 'transform.edge_bevelweight','B', 'PRESS', alt=True, value=1.0)
    add_keymap_attrs(km, 'transform.edge_bevelweight', 'B', 'PRESS', ctrl=True, alt=True)
    add_keymap_attrs(km, 'mesh.bevel','B', 'PRESS')
    add_keymap_attrs(km, 'view3d.subdivision_toggle','TAB','PRESS')   

# Map Grease Pencil
    km = get_keymap_items_ctx('Blender',  'Grease Pencil')
    add_keymap_attrs(km, 'gpencil.select_linked', 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)

# Map Image Paint
    km = get_keymap_items_ctx('Blender',  'Image Paint')
    add_keymap_attrs(km, 'paint.sample_color', 'LEFTMOUSE', 'PRESS', alt=True)

# Map Object Mode
    km = get_keymap_items_ctx('Blender',  'Object Mode')

# Map Curve
    km = get_keymap_items_ctx('Blender',  'Curve')
    add_keymap_attrs(km, 'curve.select_linked', 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)
    add_keymap_attrs(km, 'curve.select_linked_pick', 'LEFTMOUSE', 'DOUBLE_CLICK')
    add_keymap_attrs(km, 'curve.shortest_path_pick', 'LEFTMOUSE', 'PRESS', ctrl=True, shift=True)
    add_keymap_attrs(km, 'curve.draw', 'LEFTMOUSE', 'PRESS', alt=True)
    add_keymap_attrs(km, 'curve.vertex_add', 'E', 'PRESS')
    add_keymap_attrs(km, 'curve.extrude_move', 'E', 'PRESS', ctrl=True)

# Map Outliner
    km = get_keymap_items_ctx('Blender',  'Outliner')
    add_keymap_attrs(km, 'outliner.show_active', 'MIDDLEMOUSE', 'PRESS', ctrl=True, shift=True)

# Map Screen
    km = get_keymap_items_ctx('Blender',  'Screen')
    add_keymap_attrs(km, 'screen.redo_last', 'D', 'PRESS')

# Add modal keymap
    km = get_keymap_items_ctx('Blender', 'Transform Modal Map')
    modify_modal_keymap(km, add_modal_keymap={"AXIS_Y": "SPACE"}, remove_modal_keymap={"CONFIRM": "SPACE"})

def delayed_keymap_registration():
    Keymap_Register()
    return None  # Stops the timer

bpy.app.timers.register(delayed_keymap_registration, first_interval=2.0)


def register():
    Keymap_Register()

def unregister():
    Keymap_Register()

if __name__ == '__main__':
    register()
