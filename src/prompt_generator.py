# This method creates a substring of the prompt for the GPT-4 API. If the blooms taxonomy level is determined, then it
# uses a specific prompt.
# **Note: Not all levels have a prompt already implemented yet.**
# If the level is not determined at first, then GPT-4 is advised to determine it itself and adapt its own behaviour to
# the level.
def bloom_prompt_generator(self, bloom_level: object) -> str:
    # Knowledge
    if bloom_level == 0:
        prompt = """\nThe bloom level is knowledge. As an assistant you will need to check, if the student can recall 
relevant facts and basic concepts involving the questions topic area."""
    # Comprehension
    elif bloom_level == 1:
        prompt = """\nThe bloom level is comprehension. As an assistant you will need to check, if the student is able 
to explain the specified idea or concept well."""
    elif bloom_level == 2:
        prompt = """\nThe bloom level is application. The student have to apply a concept and you as an assistant 
have to check, if the student uses the right concept and if the answer of resulting of the usage is correct."""
    # Need to be prompt engineered later. We make a standardized prompt for the upper three levels: Analysis, Synthesis
    # and Evaluation
    #  elif bloom_level == 3:
    #     prompt = ("Please")
    #   elif bloom_level == 4:
    #     prompt = ("Please")
    #   elif bloom_level == 5:
    #     prompt = ("Please")
    else:
        prompt = """\nThe bloom level of the question could not be determined. As an assistant you will need to 
determine the correct bloom level. After determining the correct bloom level you will analyze the solution in 
an appropriate manner of the bloom level."""
    return prompt


# This method creates a substring of the prompt for the GPT-4 API. If keywords are supplied, the prompt will include
# them and will order the API to these words into account. If no keywords are supplied, then there will be no substring
# for that involves keywords.
def keyword_prompt_generator(self, keyword):
    prompt = ""
    if self.keyword_present:
        words = ""
        for word in keyword:
            words += word
            words += ";"
        prompt = f"""
        \nThe professor delivered some keywords, which he finds relevant to resolve the examination question.
The keywords are: {words}
        \nIn order of the evaluation, please check if these keywords are mentioned in any contextual form. If they are,
this would benefit the feedback.
        """
    return prompt


# This method creates a substring of the prompt for the GPT-4 API. If a solution is delivered the prompt will include it
# otherwise it orders GPT-4 to generate its own solution.
def example_prompt_generator(self, example_solution):
    if self.solution_present:
        prompt = f"\nThe professor delivered the following example solution:\n{example_solution}"
    else:
        prompt = """There is no example solution delivered by the professor. Generate one solution to the 
corresponding to the possible achievable points for the question."""
    return prompt


# This method generates the final prompt. It uses the specific information of the whole task and generates a prompt
# based on the information
def final_prompt_generator(self):
    step_counter = 0
    prompt_appendix_steps = ""
    if self.question[2] == "N":
        step_counter += 1
        prompt_appendix_steps += f"\n{step_counter}. Determine the taxonomy level"
    if self.keyword_present:
        step_counter += 1
        prompt_appendix_steps += f"\n{step_counter}. Check if the keywords are contextual mentioned in the answer"
    if self.solution_present:
        step_counter += 1
        prompt_appendix_steps += f"\n{step_counter}. Compare the professor solution with the answer of the student"
    else:
        step_counter += 1
        prompt_appendix_steps += f"\n{step_counter}. Compare your solution with the answer of the student"
    step_counter += 1
    prompt_appendix_steps += f"""\n{step_counter}. Evaluate if the answer of the student is right or wrong and if there 
are missing or false information please highlight them and explain, why these information are false. Don't outline the
correct information."""

    prompt = f"""You are an AI assistant that helps with the assessment of free text answers in the subject software 
engineering and programming. You will receive the question and the student answer to this question.\n{self.bloom_prompt}
\nThe examination question is: \n{self.question[0]}{self.keyword_prompt}{self.example_solution_prompt}
    \nWith all this information to will now evaluate the incoming student answer.
    \nDo the following steps:
    """
    return prompt + prompt_appendix_steps


# Basic prompt generator class. Purpose is to dynamically modify the content for the role system/assistant according to
# the question and several settings, that are included.
class PromptGenerator:
    question = {}
    keyword_present = False
    solution_present = False

    def __init__(self):
        self.bloom_prompt = ""
        self.keyword_prompt = ""
        self.example_solution_prompt = ""
        self.final_prompt = ""

    # End-point for the prompt generation. Needs the question tuple, the keyword list and the exampl solution. None of
    # the last two attributes need a value for this method to work perfectly.
    def generate_prompts(self, question, keywords, example_solution):
        self.keyword_present = len(keywords) > 0
        self.solution_present = example_solution is not None
        self.question = question
        self.bloom_prompt = bloom_prompt_generator(self, question[2])
        self.keyword_prompt = keyword_prompt_generator(self, keywords)
        self.example_solution_prompt = example_prompt_generator(self, example_solution)
        final_prompt = final_prompt_generator(self)
        return final_prompt
