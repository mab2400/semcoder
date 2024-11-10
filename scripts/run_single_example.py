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

def process_single_entry(input_csv_file_path, entry_point):
    """
    Processes a single entry specified by `entry_point`, runs the relevant tests, 
    and prints the results to the terminal.
    """
    with open(input_csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if row['entry_point'] == entry_point:
                print(f"Generating code for {entry_point}...")
                prompt = row['prompt']
                
                # Generate code based on the prompt
                generated_code = pipe(prompt, max_new_tokens=512, num_return_sequences=1)[0]['generated_text']
                row['generated_code'] = generated_code
                
                # Test the generated code using the given test cases
                test_cases = row['test_cases']
                print(f"Evaluating against given test cases...")
                result = run_example(test_cases, generated_code, entry_point)
                
                # Print the result to the terminal
                print(f"Entry Point: {entry_point}")
                print(f"Prompt: {prompt}")
                print(f"Generated Code:\n{generated_code}")
                print(f"Test Cases:\n{test_cases}")
                print(f"Result: {result}")
                print(f"Category: {row.get('category', 'N/A')}")
                return
        
        print(f"No entry found for entry point '{entry_point}'.")

# Usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SemCoder on a single entry from a CSV dataset and print results.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("entry_point", help="The entry point of the example to test")

    args = parser.parse_args()

    process_single_entry(args.input_csv, args.entry_point)
