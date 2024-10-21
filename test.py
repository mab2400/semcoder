import os
import sys
import json

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

    # Read the JSONL file
    with open(file_path, 'r') as file:
        for line in file:
            # Parse the JSON object from each line
            data = json.loads(line)

            # Extract from the prompt + test from the JSON object
            prompt = data["prompt"]
            test = data["test"]

            # Format the prompt for Python
            # Escape triple quotes and ensure it's formatted correctly
            formatted_prompt = prompt.replace('"""', '\"\"\"')
            formatted_prompts.append(formatted_prompt)

            # Store the test case as a string
            test_cases.append(test)

    return formatted_prompts, test_cases

# Load SemCoder model using the text-generation pipeline
pipe = pipeline("text-generation", model="semcoder/semcoder")

# Specify the path to your JSON file
json_file_path = 'humaneval.jsonl'

# Use the function to get formatted prompts + tests
formatted_prompts, test_cases = format_prompt_from_file(json_file_path)

# Generate code for each formatted prompt using SemCoder
for i, prompt in enumerate(formatted_prompts):
    print(f"Generating code for Prompt {i + 1}...\n")
    generated_code = pipe(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']
    print(f"Generated code for Prompt {i + 1}:\n{generated_code}\n")

    print(f"Tests for this code:\n{test_cases[i]}\n")