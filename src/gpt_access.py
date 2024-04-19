import openai

with open('.key', 'r') as file:
    # Read a line from the file
    key = file.readline().strip()
    base = file.readline().strip()
    name = file.readline().strip()

openai.api_key = key
openai.api_base = base
openai.api_type = 'azure'
openai.api_version = '2023-05-15'  # this might change in the future
deployment_name = name


def send_message(message):
    answer = openai.ChatCompletion.create(

        engine="GPT4StudentAssessment",

        messages=message,

        temperature=0.25,

        max_tokens=600,

        top_p=0.95,

        frequency_penalty=0,

        presence_penalty=0,

        stop=None
    )
    return answer['choices'][0]['message']['content']


def send_message_and_temp(message, temp):
    response = openai.Completion.create(
        engine="GPT4StudentAssessment",

        messages=message,

        temperature=temp,

        max_tokens=600,

        top_p=0.95,

        frequency_penalty=0,

        presence_penalty=0,

        stop=None
    )
    return response['choices'][0]['message']['content']
