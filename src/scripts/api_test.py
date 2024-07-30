import os
import openai
import create_dataset as cd

with open('../../server/.key', 'r') as file:
    # Read a line from the file
    key = file.readline().strip()
    base = file.readline().strip()
    name = file.readline().strip()


openai.api_key = key
openai.api_base = base
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this might chage in the future

deployment_name= name


message_text = [{"role":"system","content":"You will recieve now question, answers and the bloom taxonomy category of the questions. Please evaluate how the answers are"}]


completion = openai.ChatCompletion.create(

  engine="GPT4StudentAssessment",

  messages = message_text,

  temperature=0.7,

  max_tokens=800,

  top_p=0.95,

  frequency_penalty=0,

  presence_penalty=0,

  stop=None

)
assistant_message = completion['choices'][0]['message']['content']
print(message_text[0]['content'])
print(assistant_message)
# Send a completion call to generate an answer
    #print('Sending a test completion job')
    #start_phrase = 'Write a tagline for an ice cream shop. '
    #response = openai.ChatCompletion.create(engine=deployment_name, prompt=start_phrase, max_tokens=10)
    #text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
    #print(start_phrase+text)

data_set = cd.create_tuple_dict(cd.read_json_file("Datasets/intents.json"))
for questions in data_set:
    message_text = [{"role":"system","content":f"Question: {data_set[questions][0]} Answer: {data_set[questions][1]} Blooms Kategory: {data_set[questions][2]}"}]
    completion = openai.ChatCompletion.create(

         engine="GPT4StudentAssessment",

         messages = message_text,

         temperature=0.7,

         max_tokens=800,

         top_p=0.95,

         frequency_penalty=0,

         presence_penalty=0,

         stop=None
    )
    assistant_message = completion['choices'][0]['message']['content']
    with open("first_data_set_run.txt", "a") as file:
        file.write(assistant_message)
        file.write("\n")
print("task complete")
