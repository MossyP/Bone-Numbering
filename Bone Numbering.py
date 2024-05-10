import bpy

# プラグインに関する情報
bl_info = {
    "name" : "Melo Bone Numbering",             # プラグイン名
    "author" : "Mossy",                  # 作者
    "version" : (0,1),                  # プラグインのバージョン
    "blender" : (3, 6, 0),              # プラグインが動作するBlenderのバージョン
    "location" : "View3D > Tool",   # Blender内部でのプラグインの位置づけ
    "description" : "Add prefix or subfix",   # プラグインの説明
    "warning" : "",
    "wiki_url" : "",                    # プラグインの説明が存在するWikiページのURL
    "tracker_url" : "",                 # Blender Developer OrgのスレッドURL
    "category" : "Rigging"                   # プラグインのカテゴリ名
}



class OBJECT_OT_BoneNumberingAddon(bpy.types.Operator):
    bl_idname = "object.bone_numbering"
    bl_label = "Number Selected Bones"
    bl_options = {'REGISTER', 'UNDO'}

    start_number: bpy.props.IntProperty(
        name="Start Number",
        default=1,
        min=1,
        description="The starting number for the bone numbering"
    )

    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ('PREFIX', "Prefix", "Add prefix to selected bones"),
            ('SUBFIX', "Subfix", "Add subfix to selected bones")
        ],
        default='PREFIX'
    )

    @staticmethod
    def is_edit_mode(context):
        return context.mode == 'EDIT_ARMATURE'

    def execute(self, context):
        if not self.is_edit_mode(context):
            self.report({'WARNING'}, "This operator can only be used in Edit mode of an armature.")
            return {'CANCELLED'}

        bones = context.selected_bones
        if bones:
            if self.mode == 'PREFIX':
                for i, bone in enumerate(bones, self.start_number):
                    new_name = str(i) + "_" + bone.name
                    if new_name != bone.name:
                        bone.name = new_name
            elif self.mode == 'SUBFIX':
                for i, bone in enumerate(bones, self.start_number):
                    new_name = bone.name + "_" + str(i)
                    if new_name != bone.name:
                        bone.name = new_name
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_ARMATURE'

class VIEW3D_PT_BoneNumberingPanel(bpy.types.Panel):
    bl_label = "Melo's Bone Numbering"
    bl_category = "Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("object.bone_numbering", text="Apply")

class BoneNumberingProps(bpy.types.PropertyGroup):
    start_number: bpy.props.IntProperty(
        name="Start Number",
        default=1,
        min=1,
        description="The starting number for the bone numbering"
    )

    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ('PREFIX', "Prefix", "Add prefix to selected bones"),
            ('SUBFIX', "Subfix", "Add subfix to selected bones")
        ],
        default='PREFIX'
    )

def register():
    bpy.utils.register_class(OBJECT_OT_BoneNumberingAddon)
    bpy.utils.register_class(VIEW3D_PT_BoneNumberingPanel)
    bpy.utils.register_class(BoneNumberingProps)
    bpy.types.Scene.bone_numbering_props = bpy.props.PointerProperty(type=BoneNumberingProps)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_BoneNumberingAddon)
    bpy.utils.unregister_class(VIEW3D_PT_BoneNumberingPanel)
    bpy.utils.unregister_class(BoneNumberingProps)
    del bpy.types.Scene.bone_numbering_props

if __name__ == "__main__":
    register()
