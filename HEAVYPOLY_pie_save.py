import bpy
from bpy.types import Menu

class HP_MT_pie_save(Menu):
	bl_label = "Save"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		pie.operator("wm.link", text = "Link/Reference", icon='LINK_BLEND')
		pie.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
		pie.operator("wm.save_as_mainfile", text="Save As...", icon='NONE')
		pie.operator("wm.open_mainfile", text="Open file", icon='FILE_FOLDER')
		pie.operator("wm.read_homefile", text="New", icon='FILE_NEW')
		pie.separator()
		pie.menu("TOPBAR_MT_file_open_recent")

def save_register():
	bpy.utils.register_class(HP_MT_pie_save)

def save_unregister():
	bpy.utils.unregister_class(HP_MT_pie_save)