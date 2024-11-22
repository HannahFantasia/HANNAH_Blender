import bpy
import json
import os
import ast

# Track keymap items per context
keymap_registered_addon = []
keymap_unregistered_addon = []


# JSON Parsing and Keymap Context Generation
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


# Get info from JSON and make sure there is no duplicate tuples, desired output: [('Blender', 'Animation'), ('Blender', 'Dopesheet')] 
def json_context_to_list(json_data):

    unique_contexts = set()
    excluded_entry = ("Blender", "Transform Modal Map")

    for section in json_data.values():
        for entry in section:
            config_context = (entry.get("keymap_config"), entry.get("keymap_context"))
            if config_context != (None, None) and config_context != excluded_entry:
                unique_contexts.add(config_context)

    unique_contexts_list = list(unique_contexts)
    return unique_contexts_list

# Utility function for keymap management 
def get_keymap_items_ctx(keymap_config: str, keymap_context: str):
    return bpy.context.window_manager.keyconfigs[keymap_config].keymaps[keymap_context].keymap_items


# Utility function to convert json strings to sets 
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


# Function to add keymaps based on arguments
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
    keymap_item = keymap_items_context.new(
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
        if hasattr(keymap_item.properties, prop_key):
            setattr(keymap_item.properties, prop_key, prop_value)

    return [keymap_config, keymap_context, keymap_item]


# Function to remove keymaps based on arguments 
def remove_keymap_attrs(keymap_config: str,
                        keymap_context: str,
                        idname: str,
                        event_type: str, 
                        value_key: str,
                        **kwargs):
    
    keymap_items_context = get_keymap_items_ctx(keymap_config, keymap_context)

    for keymap_item in keymap_items_context:
        if keymap_item.idname == idname and keymap_item.type == event_type and value_key == keymap_item.value:
            keymap_items_context.remove(keymap_item)
            return [keymap_config, keymap_context, keymap_item]


# add Addon Keys from JSON (use in register)
def add_addon_keys():
    keymap_attrs_data = convert_sets(json_content.get("add_keymap_attrs", []))
    if not add_keymap_attrs:
        print("Warning: No 'add_keymap_attrs' found in the JSON content.")
        return

    # Process addon keys
    for keymap in keymap_attrs_data:
        try:
            # Pass the JSON keymap data to add_keymap_attrs
            keymap_added = add_keymap_attrs(**keymap)
            keymap_registered_addon.append(keymap_added)
        except Exception as e:
            print(f"Error adding Addon keymap: {e}")


# Remove Addon Keys from JSON (use in register)
def remove_addon_keys():
    keymap_attrs_data = convert_sets(json_content.get("remove_keymap", []))
    if not keymap_attrs_data:
        print("Warning: No 'remove_keymap' found in the JSON content.")
        return

    # Process addon keys
    for keymap in keymap_attrs_data:
        try:
            # Pass the JSON keymap data to add_keymap_attrs
            keymap_removed = remove_keymap_attrs(**keymap)
            keymap_unregistered_addon.append(keymap_removed)
        except Exception as e:
            print(f"Error removing Addon keymap: {e}")

# remove created addon keys from list (used as a restore for default keymaps in unregister)
def remove_addon_keys_from_list():
    for keymap in keymap_registered_addon[:]:
        keymap_config, keymap_context, keymap_item = keymap
        remove_keymap_attrs(
            keymap_config=keymap_config,
            keymap_context=keymap_context,
            idname=keymap_item.idname,
            event_type=keymap_item.type,
            value_key=keymap_item.value
        )
        keymap_registered_addon.remove(keymap)

# restore removed addon keys from list (used as a restore for default keymaps in unregister)
def add_addon_keys_from_list():
    for keymap in keymap_unregistered_addon[:]:
        keymap_config, keymap_context, keymap_item = keymap
        add_keymap_attrs(
            keymap_config=keymap_config,
            keymap_context=keymap_context,
            idname=keymap_item.idname,
            event_type=keymap_item.type,
            value_key=keymap_item.value
        )
        keymap_unregistered_addon.remove(keymap)


# A bunch of variables that are going to be used later on. 
script_dir = os.path.dirname(__file__) # directory of the file that launches the script
json_file_path = 'keymaps.json' # file name
json_file_path_os = os.path.join(script_dir, json_file_path) # full path

json_content = parse_json(json_file_path_os) # parse JSON
add_json_context = json_context_to_list(json_content) # turn JSON config and context into list


add_addon_keys()
print("keymap_registered_addon:", keymap_registered_addon)
remove_addon_keys_from_list()
print("keymap_registered_addon:", keymap_registered_addon)