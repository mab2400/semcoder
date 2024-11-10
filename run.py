import csv
import sys

# Path to CSV file containing 'test_cases', 'generated_code', 'entry_point', and 'all_tests_passed' columns
csv_file_path = 'test_results_pass_fail.csv'

def run_example(test_cases, generated_code, entry_point):
    """
    Runs a single example by executing the test cases on the generated code, extracting only relevant portions.
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
        return "Passed"  # All tests passed
    except AssertionError as e:
        print(f"Assertion failed: {e}\n")
        return "Failed"  # Test failed
    except Exception as e:
        print(f"An error occurred: {e}\n")
        return "Error"  # Error occurred

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

def process_all_entries():
    """
    Processes each entry in the CSV, runs the relevant tests, updates the pass/fail status, and writes back to the CSV.
    """
    updated_rows = []
    total_entries = 0
    pass_count = 0

    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for i, row in enumerate(reader):
            print(f"Processing entry {i + 1}:")
            total_entries += 1

            test_cases = row['test_cases']
            generated_code = row['generated_code']
            entry_point = row['entry_point']

            result = run_example(test_cases, generated_code, entry_point)
            row['all_tests_passed'] = result
            if result == "Passed":
                pass_count += 1

            updated_rows.append(row)

    with open(csv_file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    pass_percentage = (pass_count / total_entries) * 100 if total_entries > 0 else 0
    print(f"CSV file updated with pass/fail results.")
    print(f"Pass Percentage: {pass_percentage:.2f}% ({pass_count} out of {total_entries})")

# Usage
if __name__ == "__main__":
    if len(sys.argv) == 2:
        entry_point = sys.argv[1]
        run_single_test(entry_point)
    else:
        process_all_entries()
