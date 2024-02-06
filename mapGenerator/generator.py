# RUN:
# blender -b -P generator.py

import bpy
import os

def main():
    sample = [{"path": "/Users/LENOVO/Desktop/blender_test/cube.blend", "pos": [5, 5, 0]},
            {"path": "/Users/LENOVO/Desktop/blender_test/sphere.blend", "pos": [0, 0, 0]}]
    import_and_generate(sample, "output_3d_file.blend")


def import_and_generate(targets_dict, output_path):
    # Clear existing mesh objects in the scene
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new Blender file
    bpy.ops.wm.save_as_mainfile(filepath=output_path)

    # Import each blend file and place it at the specified position
    for target in targets_dict:

        blend_file = target["path"]
        position = target["pos"]

        # Append the entire data block from the blend file
        with bpy.data.libraries.load(blend_file) as (data_from, data_to):
            data_to.objects = data_from.objects

        # Create a new collection for each blend file
        new_collection = bpy.data.collections.new(
            name=os.path.basename(blend_file))
        bpy.context.scene.collection.children.link(new_collection)

        # Link or append objects to the new collection
        for obj in data_to.objects:
            if obj is not None:
                new_collection.objects.link(obj)

        # Adjust the imported objects' position
        for obj in new_collection.objects:
            obj.location = position

    # Save the final blend file
    bpy.ops.wm.save_as_mainfile(filepath=output_path)


if __name__ == '__main__':
    main()