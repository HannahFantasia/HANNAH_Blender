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

    try:
        for section in json_data.values():
            for entry in section:
                config_context = (entry.get("keymap_config"), entry.get("keymap_context"))
                if config_context != (None, None) and config_context != excluded_entry:
                    unique_contexts.add(config_context)
    except Exception as e:
        print(f"An error occurred: {e}")

    unique_contexts_list = list(unique_contexts)
    return unique_contexts_list

# A bunch of variables that are going to be used later on. (COMPLETED)
script_dir = os.path.dirname(__file__) # directory of the file that launches the script
json_file_path = 'keymaps.json' # file name
json_file_path_os = os.path.join(script_dir, json_file_path) # full path

json_content = parse_json(json_file_path_os) # parse JSON
add_json_context = json_context_to_list(json_content) # turn JSON config and context into list


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


# Utility function for keymap management 
def get_keymap_items_ctx(keymap_config: str, keymap_context: str):
    return bpy.context.window_manager.keyconfigs[keymap_config].keymaps[keymap_context].keymap_items


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
    try:
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
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        # Set properties for the keymap item through kwargs
        for prop_key, prop_value in kwargs.items():
            if hasattr(keymap_item.properties, prop_key):
                setattr(keymap_item.properties, prop_key, prop_value)
    except Exception as e:
        print(f"An error occurred: {e}")

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
        try:
            if keymap_item.idname == idname and keymap_item.type == event_type and value_key == keymap_item.value:
                keymap_items_context.remove(keymap_item)
                return [keymap_config, keymap_context, keymap_item]
        except Exception as e:
            print(f"An error occurred: {e}")


# Function to add modal keymaps based on arguments
def add_modal_attrs(keymap_config: str,
                    keymap_context: str,
                    propvalue: str,
                    event_type: str,
                    value_key: str,
                    **kwargs):
    # retrieve the keymap items context
    keymap_items_context = get_keymap_items_ctx(keymap_config, keymap_context)
    
    try:
        keymap_items_context.new_modal(propvalue, event_type, value_key, **kwargs)
        return [keymap_config, keymap_context, propvalue, event_type, value_key]
    except Exception as e:
        print(f"An error occurred: {e}")


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
        try:
            if keymap_item.propvalue == propvalue and keymap_item.type == event_type and keymap_item.value == value_key:
                keymap_items_context.remove(keymap_item)
                return [keymap_config, keymap_context, propvalue, event_type, value_key]
        except Exception as e:
            print(f"An error occurred: {e}")
###### ADDON KEYMAPS ######

# add Addon Keys from JSON (use in register)
def add_addon_keys():
    keymap_attrs_data = convert_sets(json_content.get("add_keymap_attrs", []))
    if not keymap_attrs_data:
        print("Warning: No 'add_keymap_attrs' found in the JSON content.")
        return

    # Process addon keys
    for keymap in keymap_attrs_data:
        try:
            # Pass the JSON keymap data to add_keymap_attrs
            add_keymap_attrs(**keymap)
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
            remove_keymap_attrs(**keymap)
        except Exception as e:
            print(f"Error removing Addon keymap: {e}")


# remove created addon keys from list (used as a restore for default keymaps in unregister)
def remove_addon_keys_from_json():
    keymap_attrs_data = convert_sets(json_content.get("add_keymap_attrs", []))
    if not keymap_attrs_data:
        print("Warning: No 'add_keymap_attrs' found in the JSON content.")
        return

    # Process addon keys
    for keymap in keymap_attrs_data:
        try:
            # Pass the JSON keymap data to add_keymap_attrs
            remove_keymap_attrs(**keymap)
        except Exception as e:
            print(f"Error adding Addon keymap: {e}")


# restore removed addon keys from list (used as a restore for default keymaps in unregister)
def add_addon_keys_from_json():
    keymap_attrs_data = convert_sets(json_content.get("remove_keymap", []))
    if not keymap_attrs_data:
        print("Warning: No 'remove_keymap' found in the JSON content.")
        return
    
    # Process addon keys
    for keymap in keymap_attrs_data:
        try:
            # Pass the JSON keymap data to add_keymap_attrs
            add_keymap_attrs(**keymap)
        except Exception as e:
            print(f"Error restoring Addon keymap: {e}")


###### GLOBAL KEYMAPS ######


# add Global Keys from JSON (use in register)
def add_global_keys(add_json_context):
    global_keys_data = json_content.get("global_keys", [])
    if not global_keys_data:
        print("Warning: No 'global_keys' found in the JSON content.")
        return

    # Process global keys
    for keymap_config, keymap_context in add_json_context:
        for keymap in global_keys_data:
            try:
                # Pass the JSON keymap data to add_keymap_attrs
                add_keymap_attrs(keymap_config, keymap_context, **keymap)
            except Exception as e:
                print(f"Error adding Global keymap: {e}")


# remove created global keys from list (used as a restore for default keymaps in unregister)
def remove_global_keys_from_json():
    global_keys_data = json_content.get("global_keys", [])
    if not global_keys_data:
        print("Warning: No 'global_keys' found in the JSON content.")
        return

    # Process global keys
    for keymap_config, keymap_context in add_json_context:
        for keymap in global_keys_data:
            try:
                # Pass the JSON keymap data to add_keymap_attrs
                remove_keymap_attrs(keymap_config, keymap_context, **keymap)
            except Exception as e:
                print(f"Error adding Global keymap: {e}")



###### MODAL KEYMAPS ######


# add Modal Keys from JSON (use in register)
def add_modal_keys():
    # Ensure "add_modal_keymap" exists in the JSON content
    keymap_modal_data = json_content.get("add_modal_keymap", [])
    if not keymap_modal_data:
        print("Warning: No 'add_modal_keymap' found in the JSON content.")
        return
    
    for keymap in keymap_modal_data:
        try:
            # Pass the JSON keymap data to add_modal_attrs
            add_modal_attrs(**keymap)
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


# remove created modal keymaps from JSON (used as a restore for default keymaps in unregister)
def remove_modal_keys_from_json():
    keymap_modal_data = convert_sets(json_content.get("add_modal_keymap", []))
    if not keymap_modal_data:
        print("Warning: No 'add_modal_keymap' found in the JSON content.")
        return
    
    # Process modal keys
    for keymap in keymap_modal_data:
        try:
            # Pass the JSON keymap data to remove_modal_attrs
            remove_modal_attrs(**keymap)
        except Exception as e:
            print(f"Error removing Modal keymap: {e}")


# add created modal keymaps to JSON (used as a restore for default keymaps in unregister)
def add_modal_keys_from_json():
    keymap_modal_data = convert_sets(json_content.get("remove_modal_keymap", []))
    if not keymap_modal_data:
        print("Warning: No 'remove_modal_keymap' found in the JSON content.")
        return
    
    # Process modal keys
    for keymap in keymap_modal_data:
        try:
            # Pass the JSON keymap data to add_modal_attrs
            add_modal_attrs(**keymap)
        except Exception as e:
            print(f"Error restoring Modal keymap: {e}")


###### REGISTER AND UNREGISTER FUNCTIONS ######

# Keymap Register/Unregister Functions
def keymap_register():

    add_addon_keys()
    remove_addon_keys()

    add_global_keys(add_json_context)

    add_modal_keys()
    remove_modal_keys()
    print("Keymaps registered successfully.")


# Keymap Unregister Function (UPDATED)
def keymap_unregister():
    remove_addon_keys_from_json()
    add_addon_keys_from_json()

    remove_global_keys_from_json()

    remove_modal_keys_from_json()
    add_modal_keys_from_json()

    print("Keymaps unregistered successfully.")




# Register and Unregister Functions
def register():
    keymap_register()

def unregister():
    keymap_unregister()

if __name__ == '__main__':
    register()
