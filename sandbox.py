
import bpy
import json
import os
import ast

# Track keymap items per context
keymap_list = {}

# Utility function for keymap management (COMPLETED)
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

def add_addon_keys():

    # Ensure "global_keys" exists in the JSON content
    keymap_attrs_data = convert_sets(json_content.get("add_keymap_attrs", []))
    if not keymap_attrs_data:
        print("Warning: No 'add_keymap_attrs' found in the JSON content.")
        return

    # Process addon keys
    for keymap in keymap_attrs_data:
        try:
            # Pass the JSON keymap data to add_keymap_attrs
            add_keymap_attrs(
                **keymap
            )
        except Exception as e:
            print(f"Error adding keymap: {keymap}, Error: {e}")

def keymap_register():
    add_addon_keys()
    print(keymap_list)

keymap_register()