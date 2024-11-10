import csv
import sys

# Path to CSV file containing 'test_cases', 'generated_code', 'entry_point', and 'all_tests_passed' columns
csv_file_path = 'test_results_pass_fail.csv'

def run_example(test_cases, generated_code, entry_point):
    """
    Runs a single example by executing the test cases on the generated code.
    """
    code_to_run = f"""
{generated_code}

{test_cases}

check({entry_point})
"""
    local_scope = {}

    try:
        exec(generated_code, local_scope, local_scope)
        exec(test_cases, local_scope, local_scope)
        exec(f"check({entry_point})", local_scope, local_scope)
        print("All assertions passed!\n")
        return "Passed"
    except AssertionError as e:
        print(f"Assertion failed: {e}\n")
        return "Failed"
    except Exception as e:
        print(f"An error occurred: {e}\n")
        return "Error"

def run_single_test(entry_point):
    """
    Runs a single test specified by the entry point by locating it in the CSV and then testing it.
    """
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['entry_point'] == entry_point:
                test_cases = row['test_cases']
                generated_code = row['generated_code']
                result = run_example(test_cases, generated_code, entry_point)
                print(f"Result for {entry_point}: {result}")
                return

        print(f"No entry found for entry point '{entry_point}'.")

# Usage
if __name__ == "__main__":
    if len(sys.argv) == 2:
        entry_point = sys.argv[1]
        run_single_test(entry_point)
    else:
        print("Usage: python run_single_example.py <entry_point>")
