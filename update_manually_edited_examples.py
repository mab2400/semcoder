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

# Load SemCoder model using the text-generation pipeline
pipe = pipeline("text-generation", model="semcoder/semcoder")

# Paths to your JSON and CSV files
json_file_path = 'humaneval_no_examples.jsonl'  # Cleaned JSONL file with examples removed
csv_file_path = 'test_results_removed_examples.csv'

# Function to read new JSONL entries
def load_new_entries(file_path):
    entries = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            entry_point = data["entry_point"]
            prompt = data["prompt"]
            test = data["test"]
            
            entries.append({
                'entry_point': entry_point,
                'formatted_prompt': prompt,
                'test_cases': test
            })
    return entries

# Read the new JSONL data
new_entries = load_new_entries(json_file_path)

# Load existing CSV data into a dictionary for quick lookups and updates
csv_data = {}
if os.path.exists(csv_file_path):
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            csv_data[row['entry_point']] = row

# Open CSV file for updating
with open(csv_file_path, mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    # Iterate through each entry in the new JSONL data
    for entry in new_entries:
        entry_point = entry['entry_point']
        formatted_prompt = entry['formatted_prompt']
        test_cases = entry['test_cases']

        # Generate code using SemCoder
        print(f"Generating code for {entry_point}...")
        generated_code = pipe(formatted_prompt, max_new_tokens=512, num_return_sequences=1)[0]['generated_text']
        print(f"Generated code:\n{generated_code}\n")

        # Update the row in csv_data or create a new one if it doesn't exist
        if entry_point in csv_data:
            csv_data[entry_point].update({
                'formatted_prompt': formatted_prompt,
                'test_cases': test_cases,
                'generated_code': generated_code,
                'all_tests_passed': ''  # Leave blank for now
            })
        else:
            # Create a new row if entry point wasn't in the original CSV
            csv_data[entry_point] = {
                'entry_point': entry_point,
                'formatted_prompt': formatted_prompt,
                'test_cases': test_cases,
                'generated_code': generated_code,
                'all_tests_passed': ''  # Leave blank for now
            }

    # Write the updated rows back to the CSV
    writer.writerows(csv_data.values())

print("CSV file updated with new generated code where applicable.")
