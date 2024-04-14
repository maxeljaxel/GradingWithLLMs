import csv
import create_dataset as cds

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
            gpt_answer = row['gpt_output']

            # Check if question exists in the database
            if question in database:
                # Compare GPT answer with expected answer from the database
                expected_answer = database[question]
                if points:
                    # Compute squared error if points=True
                    # Maximum squared error is 50 -- subject to change
                    difference = abs(float(gpt_answer) - float(expected_answer))
                    squared_error = min((difference ** 2), 50)
                    squared_error_sum += squared_error
                    if squared_error == 0:
                        correctness[question] = 'Correct'
                    else:
                        correctness[question] = 'False -- evaluation off by: ' + str(difference) + ' points'
                else:
                    # Count correct answers if points=False
                    if gpt_answer == expected_answer:
                        correct_count += 1
                        correctness[question] = 'Correct'
                    else:
                        correctness[question] = 'False'
                total_questions += 1

    # Calculate percentage of correct answers
    if points:
        correctness_percentage = 1 - (squared_error_sum / (total_questions * 50)) # Max error = 50
    else:
        correctness_percentage = correct_count / total_questions

    return correctness_percentage, correctness


# TEST:
# Read database from JSON and convert it to a hashmap
database_json = cds.read_json_file('database.json')
database_dict = cds.create_tuple_dict(database_json)

# Specify the path to the GPT output CSV file
gpt_output = 'gpt_output.csv'

# Test with points=False for percentage of correct answers
result_percentage_correct, correctness_result = compare_to_database(database_dict, gpt_output, points=False)
print("Percentage of Correct Answers:", result_percentage_correct)
print("Correctness Results:", correctness_result)

# Test with points=True for squared error term calculation
result_squared_error, correctness_result = compare_to_database(database_dict, gpt_output, points=True)
print("Squared Error Term:", result_squared_error)
print("Correctness Results:", correctness_result)
