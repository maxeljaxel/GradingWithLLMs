import create_dataset as cd
import prompt_generator as pg
import gpt_access as access_point
import datetime as dt

content = pg.PromptGenerator()

data_set = cd.create_tuple_dict(cd.read_json_file("intents.json"))
for question in data_set:
    start = dt.datetime.now()
    message_text = [
        {
            "role": "system",
            "content": f"{content.generate_prompts(data_set[question], [], None)}"
        },
        {"role": "user",
         "content": f""" Answer: {data_set[question][1]} """}]
    result = access_point.send_message(message_text)
    with open("output.txt", "a") as file:
        file.write(f"Question nr: {question + 1}\nQuestion: {data_set[question][0]}\nAnswer: {data_set[question][1]}\n")
        file.write(result)
        file.write(f"\n{dt.datetime.now()-start}")
        file.write("\n********************\n")
print("Task completed")
