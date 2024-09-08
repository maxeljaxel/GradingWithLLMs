import prompt_generator as pg
import json
from datetime import datetime


def prompt_for_variables(param_names):
    values = {}
    for var in param_names:
        value = input(f"Please enter a value for {var}: ")
        values[var] = value
    return values


if __name__ == "__main__":

    variable_names = ["question", "points", "keywords", "example_solution", "word_limit"]
    collected_values = prompt_for_variables(variable_names)
    json.dumps(collected_values, indent=4)

    # Convert collected values to appropriate types
    question = collected_values["question"]
    points = float(collected_values["points"]) if collected_values["points"] else None
    keywords = collected_values["keywords"].split(",") if collected_values["keywords"] else []
    example_solution = collected_values["example_solution"]
    word_limit = int(collected_values["word_limit"]) if collected_values["word_limit"] else None

    # Generate prompt using PromptGenerator
    prompt_generator = pg.PromptGenerator()
    generated_prompt = prompt_generator.generate_prompts(question, points, keywords, example_solution, word_limit)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    with open(f"{timestamp}.txt", "w") as file:
        file.write(generated_prompt)

    print("Prompt generation completed")
