import csv
import sys

# Path to your CSV file containing 'test_cases', 'generated_code', and 'entry_point' columns
csv_file_path = 'test_results_1.csv'

def run_single_test(entry_point):
    # Read the CSV and find the entry with the specified entry_point
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Search for the specified entry_point
        for row in reader:
            if row['entry_point'] == entry_point:
                # Extract the test cases and generated code
                test_cases = row['test_cases']
                generated_code = row['generated_code']
                
                # Construct the full code to be executed
                code_to_run = f"""
{test_cases}

{generated_code}

check({entry_point})
"""
                local_scope = {}
                try:
                    # Execute the constructed code
                    exec(code_to_run, {}, local_scope)
                    print("All assertions passed!")
                except AssertionError as e:
                    print(f"Assertion failed: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                return

        print(f"No entry found for entry point '{entry_point}'.")

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_single_test.py <entry_point>")
    else:
        entry_point = sys.argv[1]
        run_single_test(entry_point)
