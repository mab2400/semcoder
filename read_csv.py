import csv

# Specify the path to your CSV file
csv_file_path = 'test_results_1.csv'

# Open the CSV file and read each row
with open(csv_file_path, mode='r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Iterate over each row and print out the generated code and its test cases
    for i, row in enumerate(reader, start=1):
        print(f"Entry {i}:")
        print("Generated Code:\n")
        print(row['generated_code'])
        print("\nTest Cases:\n")
        print(row['test_cases'])
        print("-" * 80)  # Separator line between entries for readability
