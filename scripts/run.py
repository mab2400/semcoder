# This script runs SemCoder on the given dataset (control or ablation) 
# and executes the test cases on the generated code. 
# It outputs a CSV file with the results written in. 

# Functionality:
# - Load dataset (control or ablation)
# - Run SemCoder on each example
# - Execute test cases on the generated code
# - Generate a CSV output with the generated code and pass/fail columns

import os
import sys
import csv
import argparse
from transformers import pipeline

# Load SemCoder model using the text-generation pipeline
pipe = pipeline("text-generation", model="semcoder/semcoder")

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

def process_all_entries(input_csv_file_path, output_csv_file_path, save_interval=10):
    """
    Processes each entry in the CSV, runs the relevant tests, updates the pass/fail status, 
    and writes back to the CSV. Progress is saved periodically.
    """
    updated_rows = []

    with open(input_csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for i, row in enumerate(reader):
            print(f"Processing entry {i + 1}:")

            # Generate code based on the prompt and add it to the CSV 'generated_code' cell
            prompt = row['prompt']
            row['generated_code'] = pipe(prompt, max_new_tokens=512, num_return_sequences=1)[0]['generated_text']

            # Test the generated code using the given test cases and add the pass/fail result to the CSV
            test_cases = row['test_cases']
            generated_code = row['generated_code']
            entry_point = row['entry_point']
            result = run_example(test_cases, generated_code, entry_point)
            row['all_tests_passed'] = result

            updated_rows.append(row)

            # Save progress to the CSV file every `save_interval` entries
            if (i + 1) % save_interval == 0:
                with open(output_csv_file_path, mode='w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_rows)
                print(f"Progress saved at entry {i + 1}.")

    # Final save to ensure all rows are written
    with open(output_csv_file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"CSV file updated with pass/fail results at {output_csv_file_path}")


# Usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SemCoder on a CSV dataset and save results.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file with results")

    args = parser.parse_args()

    process_all_entries(args.input_csv, args.output_csv)