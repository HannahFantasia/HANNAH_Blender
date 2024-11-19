bl_info = {
    'name': 'Hannah_Hotkeys',
    'description': 'Hotkeys',
    'author': 'Hannah Ümit',
    'version': (0, 1, 0),
    'blender': (4, 0, 0),
    'location': '',
    'warning': '',
    'wiki_url': '',
    'category': 'Hotkeys'
}

import bpy
import json
import os
import ast

# Track keymap items per context
keymap_list = {}

# Utility function for keymap management (COMPLETED)
def get_keymap_items_ctx(keymap_config: str, keymap_context: str):
    return bpy.context.window_manager.keyconfigs[keymap_config].keymaps[keymap_context].keymap_items


# Utility function to convert json strings to sets (COMPLETED)
def convert_sets(data):
    """
    Recursively convert strings that look like Python sets into actual sets.
    """
    # Process dictionary: check all key-value pairs
    if isinstance(data, dict):
        return {key: convert_sets(value) for key, value in data.items()}
    
    # Process lists: recursively check each element
    elif isinstance(data, list):
        return [convert_sets(item) for item in data]
    
    # Try to interpret strings as sets
    elif isinstance(data, str):
        try:
            if data.startswith('{') and data.endswith('}'):
                result = ast.literal_eval(data)
                if isinstance(result, set):
                    return result
        except (ValueError, SyntaxError):
            pass  # Ignore strings that aren't valid Python expressions
    return data  # Return unchanged if no conversion is needed


# Function to add keymaps based on arguments (COMPLETED)
def add_keymap_attrs(keymap_config: str,
                     keymap_context: str,
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

    keymap_items_context = get_keymap_items_ctx(keymap_config, keymap_context)

    # Create the keymap item
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

    # Set properties for the keymap item through kwargs
    for prop_key, prop_value in kwargs.items():
        if hasattr(keymap_added.properties, prop_key):
            setattr(keymap_added.properties, prop_key, prop_value)

    if keymap_context not in keymap_list:
        keymap_list[keymap_context] = []
    keymap_list[keymap_context].append(keymap_added)


# remove keymap in default Blender setup (COMPLETED)
def remove_keymap_attrs(keymap_config: str, keymap_context: str):
    keymap_items_context = get_keymap_items_ctx(keymap_config, keymap_context)

    if keymap_context not in keymap_list:
        print(f"No keymaps to remove for context: {keymap_context}")
        return

    # Remove each keymap item
    for keymap_item in keymap_list[keymap_context]:
        try:
            if keymap_item.as_pointer() != 0:  # Check if the item is still valid
                keymap_items_context.remove(keymap_item)
                print(f"Removed keymap: {keymap_item.idname} from {keymap_context}.")
            else:
                print("Keymap item is no longer valid.")
        except (ReferenceError, ValueError) as e:
            print(f"Error removing keymap item: {e}")

    keymap_list[keymap_context].clear()

# modify modal keymap in default Blender setup (COMPLETED)
def modify_modal_keymap(keymap_config: str,
                        keymap_context: str,
                        add_modal_keymap: dict = None,
                        remove_modal_keymap: dict = None):
    
    keymap_items_context = get_keymap_items_ctx(keymap_config, keymap_context)

    if add_modal_keymap:
        for item in keymap_items_context:
            property_value = item.propvalue
            if property_value in add_modal_keymap:
                item.type = add_modal_keymap[property_value]

    if remove_modal_keymap:
        for item in reversed(keymap_items_context):
            property_value = item.propvalue
            key = item.type
            if property_value in remove_modal_keymap and key == remove_modal_keymap[property_value]:
                keymap_items_context.remove(item)
    


# JSON Parsing and Keymap Context Generation (COMPLETED)
def parse_json(json_file_path):
    
    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
        if isinstance(json_data, dict):
            return json_data
        else:
            print(f"Error: Expected a dictionary, but got {type(json_data).__name__}.")
            return {}
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {json_file_path}.")
        return {}


# Get info from JSON and make sure there is no duplicate tuples, desired output: [('Blender', 'Animation'), ('Blender', 'Dopesheet')] (COMPLETED)
def json_context_to_list(json_data):

    unique_contexts = set()
    excluded_entry = ("Blender", "Transform Modal Map")

    for section in json_data.values():
        for entry in section:
            config_context = (entry.get("keymap_config"), entry.get("keymap_context"))
            if config_context != (None, None) and excluded_entry:
                unique_contexts.add(config_context)

    unique_contexts_list = list(unique_contexts)
    return unique_contexts_list

# A bunch of variables that are going to be used later on. (COMPLETED)
script_dir = os.path.dirname(__file__) # directory of the file that launches the script
json_file_path = 'keymaps.json' # file name
json_file_path_os = os.path.join(script_dir, json_file_path) # full path

json_content = parse_json(json_file_path_os) # parse JSON
add_json_context = json_context_to_list(json_content) # turn JSON config and context into list


# Add and Remove global keys (COMPLETED)
def add_remove_global_keys(add_json_context, add_remove: str):

    global_keys_data = json_content.get("global_keys", [])
    if not global_keys_data:
        print("Warning: No 'global_keys' found in the JSON content.")
        return

    # Process global keys
    for keymap_setup in add_json_context:
        for keymap in global_keys_data:
            if add_remove == "add_keymaps":
                try:
                    # Pass the JSON keymap data to add_keymap_attrs
                    add_keymap_attrs(
                        keymap_config=keymap_setup[0],
                        keymap_context=keymap_setup[1],
                        **keymap
                    )
                except Exception as e:
                    print(f"Error adding keymap: {e}")

            if add_remove == "remove_keymaps":
                try:
                    # Pass the JSON keymap data to add_keymap_attrs
                    remove_keymap_attrs(
                        keymap_config=keymap_setup[0],
                        keymap_context=keymap_setup[1]
                    )
                except Exception as e:
                    print(f"Error removing keymap: {e}")


# Add and Remove Addon Keys (COMPLETED)
def add_remove_addon_keys(add_remove: str):

    # Ensure "global_keys" exists in the JSON content
    keymap_attrs_data = convert_sets(json_content.get("add_keymap_attrs", []))
    if not keymap_attrs_data:
        print("Warning: No 'add_keymap_attrs' found in the JSON content.")
        return

    # Process addon keys
    if add_remove == "add_keymaps":
        for keymap in keymap_attrs_data:
            try:
                # Pass the JSON keymap data to add_keymap_attrs
                add_keymap_attrs(
                    **keymap
                )
            except Exception as e:
                print(f"Error adding keymap: {keymap}, Error: {e}")

    if add_remove == "remove_keymaps":
        for keymap in keymap_attrs_data:
            try:
                # Pass the JSON keymap data to add_keymap_attrs
                remove_keymap_attrs(
                    keymap
                )
            except Exception as e:
                print(f"Error adding keymap: {keymap}, Error: {e}")


def add_remove_modal_keys(add_remove: str):

    # Ensure "modify_modal_keymap" exists in the JSON content
    keymap_modal_data = convert_sets(json_content.get("modify_modal_keymap", []))
    if not keymap_modal_data:
        print("Warning: No 'add_keymap_attrs' found in the JSON content.")
        return
    
    for keymap in keymap_modal_data:
        if add_remove == "add_keymaps":
            modify_modal_keymap(
                keymap_config=keymap.get("keymap_config"),
                keymap_context=keymap.get("keymap_context"),
                add_modal_keymap=keymap.get("add_modal_keymap"),
                remove_modal_keymap=keymap.get("remove_modal_keymap"),
                )
        if add_remove == "remove_keymaps":
            modify_modal_keymap(
                keymap_config=keymap.get("keymap_config"),
                keymap_context=keymap.get("keymap_context"),
                add_modal_keymap=keymap.get("add_modal_keymap"),
                remove_modal_keymap=keymap.get("remove_modal_keymap"),
                )

# Keymap Register/Unregister Functions
def keymap_register():
    add_remove_global_keys(add_json_context, "add_keymaps")
    add_remove_addon_keys("add_keymaps")

def keymap_unregister():
    add_remove_global_keys(add_json_context, "remove_keymaps")
    add_remove_addon_keys("remove_keymaps")
    keymap_list.clear()

# Register and Unregister Functions
def register():
    keymap_register()

def unregister():
    keymap_unregister()

if __name__ == '__main__':
    register()
