import bpy
import json
import os
import ast

# Track keymap items per context
keymap_registered_modal = []
keymap_unregistered_modal = []


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


# Function to add modal keymaps based on arguments
def add_modal_attrs(keymap_config: str,
                    keymap_context: str,
                    propvalue: str,
                    event_type: str,
                    value_key: str,
                    **kwargs):
    # retrieve the keymap items context
    keymap_items_context = get_keymap_items_ctx(keymap_config, keymap_context)
    
    keymap_items_context.new_modal(propvalue, event_type, value_key, **kwargs)
    return [keymap_config, keymap_context, propvalue, event_type, value_key]


# Function to remove modal keymaps based on arguments
def remove_modal_attrs(keymap_config: str,
                       keymap_context: str,
                       propvalue: str,
                       event_type: str,
                       value_key: str):
    
    # Retrieve the keymap items context
    keymap_items_context = get_keymap_items_ctx(keymap_config, keymap_context)
    
    # Iterate through the keymap items to find the one matching the provided attributes
    for keymap_item in keymap_items_context:
        if keymap_item.propvalue == propvalue and keymap_item.type == event_type and keymap_item.value == value_key:
            keymap_items_context.remove(keymap_item)
            return [keymap_config, keymap_context, propvalue, event_type, value_key]


# add Modal Keys from JSON
def add_modal_keys():
    # Ensure "add_modal_keymap" exists in the JSON content
    keymap_modal_data = json_content.get("add_modal_keymap", [])
    if not keymap_modal_data:
        print("Warning: No 'add_modal_keymap' found in the JSON content.")
        return
    
    for keymap in keymap_modal_data:
        try:
            # Pass the JSON keymap data to add_modal_attrs
            added_map = add_modal_attrs(**keymap)
            keymap_registered_modal.append(added_map)
        except Exception as e:
            print(f"Error adding Modal keymap: {keymap}, Error: {e}")
        

# Remove Modal Keys from JSON (use in register)
def remove_modal_keys():
    # Ensure "remove_modal_keymap" exists in the JSON content
    keymap_modal_data = json_content.get("remove_modal_keymap", [])
    if not keymap_modal_data:
        print("Warning: No 'remove_modal_keymap' found in the JSON content.")
        return
    
    for keymap in keymap_modal_data:
        try:
            # Pass the JSON keymap data to remove_modal_attrs
            remove_modal_attrs(**keymap)
        except Exception as e:
            print(f"Error removing Modal keymap: {keymap}, Error: {e}")


# remove created modal keymaps from list (used as a restore for default keymaps in unregister)
def remove_modal_keys_from_list():
    for keymap in keymap_registered_modal[:]:
        remove_modal_attrs(*keymap)
        keymap_registered_modal.remove(keymap)

# add created modal keymaps to list (used as a restore for default keymaps in unregister)
def add_modal_keys_from_list():
    for keymap in keymap_unregistered_modal[:]:
        add_modal_attrs(*keymap)
        keymap_unregistered_modal.remove(keymap)

# A bunch of variables that are going to be used later on. 
script_dir = os.path.dirname(__file__) # directory of the file that launches the script
json_file_path = 'keymaps.json' # file name
json_file_path_os = os.path.join(script_dir, json_file_path) # full path

json_content = parse_json(json_file_path_os) # parse JSON
add_json_context = json_context_to_list(json_content) # turn JSON config and context into list


keymap_registered_modal.append(['Blender', 'Transform Modal Map', 'AXIS_Y', 'SPACE', 'PRESS'])
print(keymap_registered_modal)
print(keymap_unregistered_modal)
remove_modal_keys_from_list()
add_modal_keys_from_list()
print(keymap_registered_modal)
print(keymap_unregistered_modal)