import json


def load_json(filename):
    """recieves file path to open
    returns: information of file"""
    json_file = filename
    with open(json_file, 'r') as file:
        car_config = json.load(file)
    # now car_config is a dictionary equivalent to the JSON file
    return car_config
