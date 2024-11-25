import bpy
from bpy.types import Menu
from bpy.props import StringProperty

class ImportSVGAsGreasePencil(bpy.types.Operator):
    """Import an SVG file as Grease Pencil"""
    bl_idname = "import_svg.grease_pencil"
    bl_label = "Import SVG as Grease Pencil"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        name="File Path",
        description="Filepath used for importing the SVG file",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    def execute(self, context):
        # Use the Grease Pencil SVG import operator
        bpy.ops.wm.grease_pencil_import_svg(filepath=self.filepath)
        return {'FINISHED'}


    def invoke(self, context, event):
        # Open the file browser
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class HP_MT_pie_import_export(Menu):
    bl_label = "Import Export"
    def draw(self, context):
        #L
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()
        row = box.row(align=True)
        row.scale_y=1.5

        box.operator('wm.alembic_import', text='Import Alembic')
        box.operator('import_scene.fbx', text='Import FBX')
        box.operator('import_mesh.stl', text='Import STL')
        box.operator('import_scene.obj', text='Import OBJ')
        box.operator('import_image.to_plane', text='Import Image Plane')
        box.operator('import_svg.grease_pencil', text='Import SVG as Grease Pencil')
        box.operator('wm.append', text = 'Append')
        box.operator("wm.link", text = "Link")
        #R
        box = pie.split().column()  
        row = box.row(align=True)
        row.scale_y=1.5
        box.operator('wm.alembic_export', text='Export Alembic')
        box.operator('export_scene.fbx', text='Export FBX')
        box.operator('export_mesh.stl', text='Export STL')
        box.operator('export_scene.obj', text='Export OBJ')
        box.operator('image.save_as', text='Export Image')

def save_register():
    bpy.utils.register_class(HP_MT_pie_import_export)
    bpy.types.TOPBAR_MT_file_import.append(HP_MT_pie_import_export)
    bpy.utils.register_class(ImportSVGAsGreasePencil)

def save_unregister():
    bpy.utils.unregister_class(HP_MT_pie_import_export)
    bpy.types.TOPBAR_MT_file_import.remove(HP_MT_pie_import_export)
    bpy.utils.unregister_class(ImportSVGAsGreasePencil)
     