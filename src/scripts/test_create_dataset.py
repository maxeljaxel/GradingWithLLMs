import json
from server import keyword_extraction as ke


def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Die Datei konnte nicht gefunden werden.")
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)


def create_tuple_dict_with_points(data):
    """
    Is used for the _intents.json file dataset only, because it has a different structure
    :param data:
    :return:
    """
    tuple_dict = {}
    if data:
        intents = data['intents']
        for i, intent in enumerate(intents):
            points = intent['points']
            patterns = intent['patterns']
            response = intent['responses']
            for pattern, response in zip(patterns, response):
                tuple_data = (pattern, response, ke.isInBloom(pattern), int(points))
                tuple_dict[i] = tuple_data
    return tuple_dict
