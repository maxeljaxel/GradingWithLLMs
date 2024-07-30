import json
from server import keyword_extraction as ke


# Input a path to a json file
# Output the data of given json
def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Die Datei konnte nicht gefunden werden.")
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)

# Input data 
# Output Dictionary in our data format
# Watch out this function is only suitable for one specific file
def create_tuple_dict(data):
    tuple_dict = {}
    if data:
        intents = data['intents']
        for i, intent in enumerate(intents):
            tag = intent['tag']
            patterns = intent['patterns']
            responses = intent['responses']
            for pattern, response in zip(patterns, responses):
                # Tupel mit den zusätzlichen Informationen erstellen
                tuple_data = (pattern, response, ke.isInBloom(pattern))
                # Tupel dem Dictionary hinzufügen
                tuple_dict[i] = tuple_data
    return tuple_dict
