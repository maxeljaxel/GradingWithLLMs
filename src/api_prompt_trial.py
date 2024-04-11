import os
import openai
import create_dataset as cd

with open('.key', 'r') as file:
    # Read a line from the file
    key = file.readline().strip()
    base = file.readline().strip()
    name = file.readline().strip()

openai.api_key = key
openai.api_base = base
openai.api_type = 'azure'
openai.api_version = '2023-05-15'  # this might chage in the future

deployment_name = name


data_set = cd.create_tuple_dict(cd.read_json_file("intents.json"))
for number in data_set:
    message_text = [
        {
            "role": "system",
            "content": """You are an AI assistant that helps with the assessment of free text answers in the subject 
            software engineering and programming. You will receive now question, answers and the bloom taxonomy 
            category of the question. If the taxonomy is declared as N, then you have to find the the taxonomy level 
            your self. The numeration is as following ascending: Knowledge; Comprehension; Application; Analysis; 
            Synthesis; Evaluation. Please evaluate how the answers are. Your assessment is guided by the following 
            steps, but not responded in the Output: \n1. Create multiple example solution for the examination 
            question with an elaborating level corresponding to the level of knowledge required in the Blooms \n2. 
            Compare the given student answer with your example solution \n3. If the answer is not correct of the 
            student, explain and highlight the aspects that are not correct \n4. Decide wether the answers are 
            correct \n The Output should be generated as following: whether the answer is right or wrong and shortly 
            point out, missing information regarding to point 3"""
        },
        {"role": "user",
         "content": f"""Question: {data_set[number][0]} Answer: {data_set[number][1]} 
         Blooms Kategory: {data_set[number][2]}"""}]
    completion = openai.ChatCompletion.create(

        engine="GPT4StudentAssessment",

        messages=message_text,

        temperature=0.7,

        max_tokens=800,

        top_p=0.95,

        frequency_penalty=0,

        presence_penalty=0,

        stop=None
    )
    assistant_message = completion['choices'][0]['message']['content']
    with open("first_data_set_run.txt", "a") as file:
        file.write("---------------------------------------------------------------------------\n"
                   f"\n {number}.Question: {data_set[number][0]} \n\n")
        file.write(assistant_message)
        file.write("\n\n"
                   "---------------------------------------------------------------------------\n")

print("task complete")
