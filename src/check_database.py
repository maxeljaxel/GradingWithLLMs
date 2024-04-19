import json
import csv
import create_dataset as cds

# This method creates a hashmap from a JSON file, which is the output
# of GPT
def read_json_and_store(json_file):
    # Initialize an empty dictionary to store the data
    data_dict = {}

    # Read data from the JSON file
    with open(json_file, 'r') as file:
        json_data = json.load(file)

        # Check if the 'solution' key exists in the JSON data
        if 'solution' in json_data:
            solution = json_data['solution']

            # Check if the 'evaluation' key exists in the 'solution' dictionary
            if 'evaluation' in solution:
                evaluation = solution['evaluation']

                # Check if the required keys exist in the 'evaluation' dictionary
                if all(key in evaluation for key in ['correctness', 'explanation', 'missing_information', 'false_information']):
                    # Store the data in the dictionary
                    data_dict['correctness'] = evaluation['correctness']
                    data_dict['explanation'] = evaluation['explanation']
                    data_dict['missing_information'] = evaluation['missing_information']
                    data_dict['false_information'] = evaluation['false_information']
                else:
                    print("Error: Required categories missing in the evaluation.")
            else:
                print("Error: Evaluation not found in the 'solution' dictionary.")
        else:
            print("Error: Solution not found in the JSON data.")

    return data_dict


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

    # Read data from GPT output
    with open(gpt_output, 'r', newline='', encoding='utf-8') as gpt_o:
        reader = csv.DictReader(gpt_o)
        for row in reader:
            # Extract relevant values from the CSV row
            question = row['question']
            gpt_evaluation = row['gpt_output']

            # Check if question exists in the database
            found_key = None
            for key, values in database.items():
                if question in values:
                    found_key = key
                    break

            if found_key is not None:
                # Compare GPT answer with expected answer from the database
                expected_evaluation = database[found_key][3]
                if points:
                    # Compute squared error if points=True
                    # Maximum squared error is 50 -- subject to change
                    difference = abs(float(gpt_evaluation) - float(expected_evaluation))
                    squared_error = min((difference ** 2), 50)
                    squared_error_sum += squared_error
                    if squared_error == 0:
                        correctness[question] = "Correct"
                    else:
                        correctness[question] = "False -- evaluation off by: " + str(difference) + " points"
                else:
                    # Count correct answers if points=False
                    if gpt_evaluation.strip() == expected_evaluation.strip():
                        correct_count += 1
                        correctness[question] = "Correct"
                    else:
                        correctness[question] = "False"
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


# TEST:
# Read database from JSON and convert it to a hashmap
#database_json = cds.read_json_file('intents.json')
#database_dict = cds.create_tuple_dict(database_json)

# Example dictionary
database_dict = {
    0: ['Explain data abstraction.', 'Answer', 'Taxonomy', 'Correct'],
    1: ['What is software testing?', 'Answer', 'Taxonomy', 'Correct'],
    2: ['Frage2', 'Answer', 'Taxonomy', 'False'],
    3: ['Frage3', 'Answer', 'Taxonomy', 'Correct']
}

# Specify the path to the GPT output CSV file
gpt_output = 'gpt_output.csv'

# Test with points=False for percentage of correct answers
result_percentage_correct, correctness_result = compare_to_database(database_dict, gpt_output, points=False)
print("Percentage of Correct Answers:", result_percentage_correct * 100, "%")
print("Correctness Results: ", correctness_result)

# Test with points=True for squared error term calculation
#result_squared_error, correctness_result = compare_to_database(database_dict, gpt_output, points=True)
#print("Squared Error Term:", result_squared_error)
#print("Correctness Results:", correctness_result)