import json
import csv
import create_dataset as cds

# This method parses a GPT response, which can then be stored in a dictionary for comparison
def parse_gpt_response(response):
    # Parse JSON response into a Python dictionary
    response_dict = json.loads(response)

    # Extract required fields from the dictionary
    solution = response_dict['solution']
    correctness = response_dict['correctness']
    explanation = response_dict['explanation']
    missing_information = response_dict['missing_information']
    false_information = response_dict['false_information']

    return [solution, correctness, explanation, missing_information, false_information]

# This method computes the correctness of evaluations by GPT.
# It compares the expected "correctness" value from the database with
# the incoming output from GPT-4.
def compare_to_database(database, gpt_output, points=False):
    # Initialize variables for correctness counting
    total_questions = 0
    correct_count = 0
    squared_error_sum = 0

    # Hashmap for easy look-up (containing Strings)
    correctness = {}

    # Iterate over each question in the GPT output
    for index, data in database.items():
        # Compare GPT evaluation with expected evaluation
        if points:
            expected_evaluation = int(data[4][0])  # Extract expected evaluation from database
            gpt_evaluation = int(gpt_output[index][1])  # Get GPT evaluation for the question

            # Compute squared error if points=True
            difference = abs(float(gpt_evaluation) - float(expected_evaluation))
            squared_error = min((difference ** 2), 50)  # Maximum squared error is 50
            squared_error_sum += squared_error
            if squared_error == 0:
                correctness[index] = "Correct"
            else:
                correctness[index] = f"False -- evaluation off by: {difference} points"
        else:
            expected_evaluation = data[4][0].capitalize()  # Extract expected evaluation from database
            gpt_evaluation = gpt_output[index][1].capitalize()  # Get GPT evaluation for the question

            # Count correct answers if points=False
            if gpt_evaluation.strip() == expected_evaluation.strip():
                correct_count += 1
                correctness[index] = "Correct"
            else:
                correctness[index] = "False"
        total_questions += 1

    # Calculate percentage of correct answers
    if total_questions > 0:
        if points:
            correctness_percentage = 1 - (squared_error_sum / (total_questions * 50))  # Max error = 50
        else:
            correctness_percentage = correct_count / total_questions
    else:
        correctness_percentage = 0

    return correctness_percentage, correctness


'''
# TEST:

jsonString = """{
    "solution": "Software testing is a critical phase in the software development lifecycle that involves the analysis of software to confirm that it meets the required standards and to detect any defects. It serves multiple purposes: verifying that the software functions as intended, ensuring that it meets the specified requirements, and identifying any problems or bugs that need to be addressed. Testing can be conducted at different levels, such as unit testing, integration testing, system testing, and acceptance testing. It can be performed manually or with the help of automated tools. The ultimate goal of software testing is to ensure the reliability, security, and high performance of the software product.",
    "correctness": "4",
    "explanation": "",
    "missing_information": "The student's answer could be enhanced by mentioning the goals of ensuring reliability, security, and performance of the software product, which are also important aspects of software testing.",
    "false_information": ""
}"""

print(parse_gpt_response(jsonString))

# Read database from JSON and convert it to a hashmap
database_json = cds.read_json_file('intents.json')
database_dict = cds.create_tuple_dict(database_json)

gpt_json = cds.read_json_file('output.json')
gpt_dict = create_gpt_dataset(gpt_json)

result_squared_error, correctness_result = compare_to_database(database_dict, gpt_dict, points=True)
print("Correctness:", result_squared_error)
print("Correctness Results:", correctness_result)

# Test with points=False for percentage of correct answers
result_percentage_correct, correctness_result = compare_to_database(database_dict, gpt_output, points=False)
print("Percentage of Correct Answers:", result_percentage_correct * 100, "%")
print("Correctness Results: ", correctness_result)

# Test with points=True for squared error term calculation
#result_squared_error, correctness_result = compare_to_database(database_dict, gpt_output, points=True)
#print("Squared Error Term:", result_squared_error)
#print("Correctness Results:", correctness_result)
'''