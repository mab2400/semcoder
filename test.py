import os
import sys
import json
import csv

# Set cache directories
os.environ["TRANSFORMERS_CACHE"] = "/mnt/300GB-disk/huggingface_cache"
os.environ["HF_HOME"] = "/mnt/300GB-disk/huggingface_home"

# Add your package directory to the system path
sys.path.append('/mnt/300GB-disk/python_packages')

from transformers import pipeline

# Function to read and format prompts from a JSON file
def format_prompt_from_file(file_path):
    formatted_prompts = []
    test_cases = []
    entry_points = []

    # Read the JSONL file
    with open(file_path, 'r') as file:
        for line in file:
            # Parse the JSON object from each line
            data = json.loads(line)

            # Extract the prompt, test, and entry point from the JSON object
            prompt = data["prompt"]
            test = data["test"]
            entry_point = data["entry_point"]

            # Format the prompt for Python
            # Escape triple quotes and ensure it's formatted correctly
            formatted_prompt = prompt.replace('"""', '\"\"\"')
            formatted_prompts.append(formatted_prompt)

            # Store the test case as a string
            test_cases.append(test)

            # Store the entry points
            entry_points.append(entry_point)

    return formatted_prompts, test_cases, entry_points

# Function to check if a prompt result already exists in the CSV
def read_existing_code(csv_file_path):
    existing_code = {}
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Store based on entry_point, assuming it's unique
                existing_code[row['entry_point']] = row['generated_code']
    return existing_code

# Load SemCoder model using the text-generation pipeline
pipe = pipeline("text-generation", model="semcoder/semcoder")
#pipe = pipeline("text-generation", model="semcoder/semcoder", device_map="auto", offload_folder="/mnt/300GB-disk")


# Specify the path to your JSON file and CSV file
json_file_path = 'humaneval.jsonl'
csv_file_path = 'test_results_1.csv'

# Read existing CSV results
existing_code = read_existing_code(csv_file_path)

# Use the function to get formatted prompts + tests
formatted_prompts, test_cases, entry_points = format_prompt_from_file(json_file_path)

# Open CSV file in append mode
with open(csv_file_path, mode='a', newline='') as csvfile:
    fieldnames = ['entry_point', 'formatted_prompt', 'test_cases', 'generated_code', 'all_tests_passed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # If the file is empty, write the header
    if os.stat(csv_file_path).st_size == 0:
        writer.writeheader()

    # Generate code for each formatted prompt using SemCoder
    for i, prompt in enumerate(formatted_prompts):
        entry_point = entry_points[i]

        # Skip this entry if generated code already exists
        if entry_point in existing_code and existing_code[entry_point] != '':
            print(f"Skipping Prompt {i + 1}: generated code already exists.\n")
            continue

        print(f"Generating code for Prompt {i + 1}...\n")
        generated_code = pipe(prompt, max_new_tokens=512, num_return_sequences=1)[0]['generated_text']
        print(f"Generated code for Prompt {i + 1}:\n{generated_code}\n")

        # Write the results to the CSV file
        writer.writerow({
            'entry_point': entry_point,
            'formatted_prompt': formatted_prompts[i],
            'test_cases': test_cases[i],
            'generated_code': generated_code,
            'all_tests_passed': ''  # Leave this blank for now
        })

print(f"Generated code has been written to {csv_file_path}")

