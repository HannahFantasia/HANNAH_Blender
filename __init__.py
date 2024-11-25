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
    HEAVYPOLY_pie_import_export,
    HEAVYPOLY_pie_save,
    HEAVYPOLY_pie_pivots,
    HEAVYPOLY_pie_shading,
    HEAVYPOLY_pie_boolean,
    HEAVYPOLY_pie_rotate_90,
    HEAVYPOLY_pie_view,
)

# Register and Unregister Functions
def register():
    HEAVYPOLY_pie_save.save_register()
    HEAVYPOLY_pie_import_export.import_export_register()
    HEAVYPOLY_pie_shading.shading_register()
    HEAVYPOLY_pie_pivots.pivot_register()
    HEAVYPOLY_pie_boolean.boolean_register()
    HEAVYPOLY_pie_view.view_register()
    HEAVYPOLY_OPERATORS.operator_register()
    HEAVYPOLY_pie_selection.select_register()
    HEAVYPOLY_HOTKEYS.keymap_register()
    HEAVYPOLY_pie_rotate_90.rotate_90_register()

def unregister():
    HEAVYPOLY_pie_save.save_unregister()
    HEAVYPOLY_pie_import_export.import_export_unregister()
    HEAVYPOLY_pie_shading.shading_unregister()
    HEAVYPOLY_pie_boolean.boolean_unregister()
    HEAVYPOLY_pie_pivots.pivot_unregister()
    HEAVYPOLY_pie_view.view_unregister()
    HEAVYPOLY_OPERATORS.operator_unregister()
    HEAVYPOLY_pie_selection.select_unregister()
    HEAVYPOLY_HOTKEYS.keymap_unregister()
    HEAVYPOLY_pie_rotate_90.rotate_90_unregister()

if __name__ == '__main__':
    register()
