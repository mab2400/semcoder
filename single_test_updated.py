import csv
import sys

# Path to your CSV file containing 'test_cases', 'generated_code', and 'entry_point' columns
csv_file_path = 'test_results_1.csv'

def extract_relevant_code(generated_code, entry_point):
    """
    Extracts all code leading up to and including the entry point function, stopping at the end of the entry point function.
    """
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

def run_single_test(entry_point):
    # Read the CSV and find the entry with the specified entry_point
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if row['entry_point'] == entry_point:
                test_cases = row['test_cases']
                generated_code = row['generated_code']
                
                # Extract relevant code
                relevant_code = extract_relevant_code(generated_code, entry_point)
                print(f"Relevant code to execute:\n{relevant_code}\n")
                
                # Construct code to run
                code_to_run = f"""
{relevant_code}

{test_cases}

check({entry_point})
"""
                local_scope = {}
                try:
                    # Execute the relevant code to define the function
                    exec(relevant_code, local_scope, local_scope)
                    print(f"Local scope after defining relevant code: {local_scope.keys()}")

                    # Now execute the test cases
                    exec(test_cases, local_scope, local_scope)
                    print(f"Local scope after defining test cases: {local_scope.keys()}")

                    # Check if entry_point is in the local scope
                    if entry_point in local_scope:
                        print(f"Running check on {entry_point}...")
                        exec(f"check({entry_point})", local_scope, local_scope)
                        print("All assertions passed!")
                    else:
                        print(f"Function '{entry_point}' not found in local scope.")
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
