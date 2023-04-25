import pickle
import json
import os

def pickle_data(data, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(data, file)


def unpickle_data(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)
    
def pretty_print(data, items_per_line=1, indent=0, spacing=1, space=' '):
    data_list = sorted(list(data))
    max_width = max(len(str(item)) for item in data_list)
    chunks = [data_list[i:i + items_per_line] for i in range(0, len(data_list), items_per_line)]
    table = ''
    for chunk in chunks:
        formatted_chunk = [f"{item:<{max_width}}" for item in chunk]
        table += (' ' * indent) + (space * spacing).join(formatted_chunk) + '\n'
    print(table)

# given a dictionary of dictionaries, with the keys being the directory names and the values being the data to be pickled
# pickles the data in the given directory
def pickle_data_in_dir(data, dir_name, print_progress=False):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    for file_name, data in data.items():
        if not file_name.endswith(".pkl"):
            file_name += ".pkl"
        pickle_data(data, os.path.join(dir_name, file_name))
        
def convert_sets_to_sorted(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                convert_sets_to_sorted(value)
            elif isinstance(value, set):
                data[key] = sorted(value)
    elif isinstance(data, set):
        data = sorted(data)
    return data

# given a dictionary of dictionaries, with the keys being the directory names and the values being the data to be saved as JSON
def save_data_as_json(data, file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    for file_name, data in data.items():
        data = convert_sets_to_sorted(data)
        if not file_name.endswith(".json"):
            file_name += ".json"
        with open(os.path.join(file_path, file_name), "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)
