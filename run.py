import csv
import re

# Path to your CSV file containing 'test_cases', 'generated_code', 'entry_point', and 'all_tests_passed' columns
csv_file_path = 'test_results_pass_fail_2.csv'

def extract_relevant_code(generated_code, entry_point):
    """
    Extracts all code leading up to and including the entry point function, stopping at the end of the entry point function.
    """
    # Split the code by lines
    lines = generated_code.splitlines()
    relevant_code = []
    inside_function = False

    for line in lines:
        if line.startswith(f"def {entry_point}("):
            inside_function = True
        relevant_code.append(line)

        if inside_function and line.startswith("def ") and not line.startswith(f"def {entry_point}("):
            relevant_code.pop()
            break

    return "\n".join(relevant_code).strip()

# Function to format and execute each example
def run_example(test_cases, generated_code, entry_point):
    # Extract only the relevant code up to and including the entry_point function
    relevant_code = extract_relevant_code(generated_code, entry_point)
    
    # Prepare code with extracted test cases and relevant generated code
    code_to_run = f"""
{relevant_code}

{test_cases}

check({entry_point})
"""
    local_scope = {}
    
    try:
        # Execute relevant code and define function in local scope
        exec(relevant_code, local_scope, local_scope)
        
        # Define the test cases in the local scope
        exec(test_cases, local_scope, local_scope)

        # Run check on the entry point
        exec(f"check({entry_point})", local_scope, local_scope)
        
        print("All assertions passed!\n")
        return "Passed"  # All tests passed
    except AssertionError as e:
        print(f"Assertion failed: {e}\n")
        return "Failed"  # Test failed
    except Exception as e:
        print(f"An error occurred: {e}\n")
        return "Error"  # Error occurred

# Read the CSV, update pass/fail results, and write back to CSV
updated_rows = []
total_entries = 0
pass_count = 0

with open(csv_file_path, mode='r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    for i, row in enumerate(reader):
        print(f"Processing entry {i + 1}:")
        total_entries += 1

        # Extract the test cases, generated code, and entry point
        test_cases = row['test_cases']
        generated_code = row['generated_code']
        entry_point = row['entry_point']

        # Run the example and store the result in 'all_tests_passed'
        result = run_example(test_cases, generated_code, entry_point)
        row['all_tests_passed'] = result
        if result == "Passed":
            pass_count += 1
        
        # Add updated row to list
        updated_rows.append(row)

# Write updated rows back to the CSV
with open(csv_file_path, mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

# Calculate and print pass percentage
pass_percentage = (pass_count / total_entries) * 100 if total_entries > 0 else 0
print(f"CSV file updated with pass/fail results.")
print(f"Pass Percentage: {pass_percentage:.2f}% ({pass_count} out of {total_entries})")
