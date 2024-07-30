import json
from server import keyword_extraction as kwe


def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("Following Error apeard", e)

#Takes a json file (probably just 1 explicit)
#Creats a list of tuples the tuples contain a tag(id) pattern(the question), response(answer to the question), a bloom Tag(the bloom category)
def create_tuple_list(data):
    tuple_list = []
    if data:
        intents = data['intents']
        for intent in intents:
            tag = intent['tag']
            patterns = intent['patterns']
            responses = intent['responses']
            bloom_tag = kwe.get_bloom_tag(patterns)
            for pattern, response in zip(patterns, responses):
                tuple_list.append((tag, pattern, response))
    return tuple_list

# Beispielaufruf
filename = 'beispiel.json'  # Passe den Dateinamen entsprechend an
data = read_json_file(filename)

