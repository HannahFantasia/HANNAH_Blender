bl_info = {
    'name': 'Hannah_Blender',
    'description': 'Overhaul of Blender hotkeys to be friendly for left-handed users',
    'author': 'Hannah Ümit',
    'version': (0, 1, 0),
    'blender': (4, 3, 0),
    'location': '',
    'warning': '',
    'wiki_url': '',
    'category': 'User Interface'
}

import bpy

# Import modules
from . import (
    HEAVYPOLY_HOTKEYS,
    HEAVYPOLY_OPERATORS,
    HEAVYPOLY_pie_selection,
    #HEAVYPOLY_pie_areas,
    #HEAVYPOLY_pie_boolean,
    HEAVYPOLY_pie_import_export,
    #HEAVYPOLY_pie_rotate_90,
    HEAVYPOLY_pie_save,
    #HEAVYPOLY_pie_pivots,
    HEAVYPOLY_pie_shading,
    #HEAVYPOLY_pie_view
)

# Collect classes from modules
modules = [
    HEAVYPOLY_OPERATORS.classes,
    HEAVYPOLY_pie_selection.classes,
    #HEAVYPOLY_pie_areas.classes,
    #HEAVYPOLY_pie_boolean.classes,
    #HEAVYPOLY_pie_rotate_90.classes,
    #HEAVYPOLY_pie_pivots.classes,
    #HEAVYPOLY_pie_view.classes
]

# Register and Unregister Functions
def register():
    HEAVYPOLY_pie_save.save_register()
    HEAVYPOLY_pie_import_export.save_register()
    HEAVYPOLY_pie_shading.save_register()
    bpy.types.VIEW3D_MT_object.append(HEAVYPOLY_OPERATORS.menu_func)

    for cls in modules:
        for c in cls:
            try:
                bpy.utils.register_class(c)
            except Exception as e:
                print(f"Failed to register {c}: {e}")
    HEAVYPOLY_HOTKEYS.keymap_register()

def unregister():
    HEAVYPOLY_pie_save.save_unregister()
    HEAVYPOLY_pie_import_export.save_unregister()
    HEAVYPOLY_pie_shading.save_unregister()
    bpy.types.VIEW3D_MT_object.append(HEAVYPOLY_OPERATORS.menu_func)
    for cls in modules:
        for c in cls:
            try:
                bpy.utils.unregister_class(c)
            except Exception as e:
                print(f"Failed to unregister {c}: {e}")
    HEAVYPOLY_HOTKEYS.keymap_unregister()

if __name__ == '__main__':
    register()
