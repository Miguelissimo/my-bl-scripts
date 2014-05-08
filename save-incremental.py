bl_info = {
           'name':'SaveIncOperator',
           'category':'User',
           'author':'miguel'
           }

import bpy
import string

class SaveIncOperator(bpy.types.Operator):
    bl_idname = "object.save_incremental"
    bl_label = "Save scene incrementally"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        # get current blender file name
        blend_name = bpy.path.basename(bpy.data.filepath)
        print('blend_name: ', blend_name)
        
        # remove file extension
        name = blend_name[0:(len(blend_name) -6)]
        print('name: ' + name)
        
        if len(name) == 0:
            name = 'untitled'
        
        # check last digits
        digit_counter = 0
        for i in range(len(name))[::-1]:
            if name[i].isdigit():
                digit_counter += 1
                continue
            else:
                break
        
        print('digits_counter: ', digit_counter)
        if digit_counter == 0:
            new_file_name = name + '001.blend'
            print('new_file_name: ', new_file_name)
        else:
            # extract number from file name
            file_number = ''.join(name[-digit_counter:])
            print('file_number: ', file_number)
            
            # convert number to int
            number = int(file_number)
            print('number: ', number)
            
            # the increment step
            number += 1
            
            # setup new file name
            new_file_name = name[0:(len(name)-digit_counter)] + ('%03.d' % number) + '.blend'
            print('new_file_name: ', new_file_name)
        
        # extract blender file name from path
        path = bpy.data.filepath[:-len(blend_name)]
        print('Path to file %s' % path)
        
        if len(path) <= 0:
            final_path = '/home/miguel/' + new_file_name
            print('final_path: ', final_path)
        else:
            final_path = path + new_file_name
        bpy.ops.wm.save_as_mainfile(filepath=final_path, check_existing=False)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SaveIncOperator)


def unregister():
    bpy.utils.unregister_class(SaveIncOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.save_incremental()
