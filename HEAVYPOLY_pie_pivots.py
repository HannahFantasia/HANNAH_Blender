import bpy
from bpy.types import Menu

class HP_MT_pie_pivots(Menu):
    bl_label = "Pivots Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        prop = pie.operator("wm.context_toggle_enum", text="Direction", icon='OBJECT_DATA')
        prop.data_path = "scene.transform_orientation_slots[0].type"
        prop.value_1 = "NORMAL"
        prop.value_2 = "GLOBAL"


        # 6 - RIGHT
        pie.split()
        # 2 - BOTTOM

        prop = pie.operator("wm.context_set_enum", text="Pivot Individuals", icon='PIVOT_INDIVIDUAL')
        prop.data_path = "scene.tool_settings.transform_pivot_point"
        prop.value = 'INDIVIDUAL_ORIGINS'
		
        prop = pie.operator("wm.context_set_enum", text="Pivot Median", icon='PIVOT_MEDIAN')
        prop.data_path = "scene.tool_settings.transform_pivot_point"
        prop.value = 'MEDIAN_POINT'

        prop = pie.operator("wm.context_set_enum", text="Pivot Last Selected", icon='PIVOT_ACTIVE')
        prop.data_path = "scene.tool_settings.transform_pivot_point"
        prop.value = 'ACTIVE_ELEMENT'

        prop = pie.operator("wm.context_set_enum", text="Pivot Cursor", icon='PIVOT_CURSOR')
        prop.data_path = "scene.tool_settings.transform_pivot_point"
        prop.value = 'CURSOR'
        # 8 - TOP
        prop = pie.operator("transform.create_orientation", text="Pivot Custom", icon='FACESEL')
        prop.use = True
        prop.name = "Pivot Custom"
        prop.overwrite = True
        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT
        pie.operator("transform.shear", text="Shear")
        # 1 - BOTTOM - LEFT


        # 3 - BOTTOM - RIGHT


def pivot_register():
        bpy.utils.register_class(HP_MT_pie_pivots)
        bpy.types.TOPBAR_MT_file_import.append(HP_MT_pie_pivots)

def pivot_unregister():
    bpy.utils.unregister_class(HP_MT_pie_pivots)
    bpy.types.TOPBAR_MT_file_import.remove(HP_MT_pie_pivots)