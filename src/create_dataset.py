import json
import keyword_extraction as ke
def read_json_file(filename):    
try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Die Datei konnte nicht gefunden werden.")
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)

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
                tuple_data = (tag, pattern, response, "bloom")
                # Tupel dem Dictionary hinzufügen
                tuple_dict[i] = tuple_data
    return tuple_dict
