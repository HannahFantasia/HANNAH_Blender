import bpy, bmesh
from bpy.types import (
		Menu,
		Operator,
		)
import os
class HP_MT_pie_rotate90(Menu):
	bl_label = "Rotate_90"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		# left
		pie.operator('view3d.rotate_90_and_flatten', text = 'Side', icon="CENTER_ONLY").direction = 'FX'
		# right
		pie.operator('view3d.rotate_90_and_flatten', text = 'Side', icon="FILE_REFRESH").direction = 'RX'

		pie.split()
		pie.split()

		pie.operator('view3d.rotate_90_and_flatten', text = 'Front', icon="CENTER_ONLY").direction = 'FY'

		pie.operator('view3d.rotate_90_and_flatten', text = 'Front', icon="FILE_REFRESH").direction = 'RY'

		# bottomleft
		pie.operator('view3d.rotate_90_and_flatten', text = 'Top', icon="CENTER_ONLY").direction = 'FZ'
		# bottomright
		pie.operator('view3d.rotate_90_and_flatten', text = 'Top', icon="FILE_REFRESH").direction = 'RZ'


class HP_OT_rotate_90_and_flatten(bpy.types.Operator):
	bl_idname = "view3d.rotate_90_and_flatten"
	bl_label = ""
	bl_options = {'REGISTER', 'UNDO'}
	direction: bpy.props.StringProperty(name="Direction")

	def execute(self, context):
		vertmode = False
		if context.object.type == 'MESH' and context.object.mode == 'EDIT':
			obj = bpy.context.object.data
			mesh = bpy.context.object.data
			totface = mesh.total_face_sel
			totedge = mesh.total_edge_sel
			totvert = mesh.total_vert_sel

			bm = bmesh.from_edit_mesh(obj)
			if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):		
				if totvert == 1:
					vertmode = True
					print('single vert selected')
					scenepivot = bpy.context.scene.tool_settings.transform_pivot_point
					bpy.ops.view3d.snap_cursor_to_selected()
					bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
					bpy.ops.object.vertex_group_add()
					bpy.ops.object.vertex_group_assign()
					bpy.ops.mesh.select_linked(delimit=set())
			if totvert == 0:
				try:
					bpy.ops.mesh.select_all(action='SELECT')
				except:
					print('Object Mode')
#Rotate 90
		if self.direction == 'RZ':
			bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
		if self.direction == 'RY':
			bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))
		if self.direction == 'RX':
			bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))

#Flattens
		if self.direction == 'FX':
			bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), orient_matrix_type='GLOBAL')
		if self.direction == 'FY':
			bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), orient_matrix_type='GLOBAL')
		if self.direction == 'FZ':
			bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), orient_matrix_type='GLOBAL')
		if vertmode == True:
			bpy.ops.mesh.select_all(action='DESELECT')
			bpy.ops.object.vertex_group_select()
			bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)
			bpy.context.scene.tool_settings.transform_pivot_point = scenepivot
		return {'FINISHED'}
	

def rotate_90_register():
	bpy.utils.register_class(HP_MT_pie_rotate90)
	bpy.utils.register_class(HP_OT_rotate_90_and_flatten)
	bpy.types.TOPBAR_MT_file_import.append(HP_MT_pie_rotate90)

def rotate_90_unregister():
	bpy.utils.unregister_class(HP_MT_pie_rotate90)
	bpy.utils.unregister_class(HP_OT_rotate_90_and_flatten)
	bpy.types.TOPBAR_MT_file_import.remove(HP_MT_pie_rotate90)