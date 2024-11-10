import csv
import sys
from collections import defaultdict

def calculate_results(input_csv_file_path):
    """
    Calculates the overall pass percentage and category-wise pass percentage.
    
    Parameters:
    - input_csv_file_path (str): Path to the input CSV file containing 'category' and 'all_tests_passed' columns.
    
    Output:
    - Prints the overall pass percentage and category-wise pass percentage.
    """
    # Initialize counters
    total_entries = 0
    total_passed = 0
    category_counts = defaultdict(lambda: {"total": 0, "passed": 0})

    # Read the CSV file
    with open(input_csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row to count passes and categorize results
        for row in reader:
            total_entries += 1
            category = row['category']
            test_result = row['all_tests_passed']

            # Update total and pass counts
            category_counts[category]["total"] += 1
            if test_result == "Passed":
                total_passed += 1
                category_counts[category]["passed"] += 1

    # Calculate overall pass percentage
    overall_pass_percentage = (total_passed / total_entries) * 100 if total_entries > 0 else 0

    # Print overall results
    print(f"Overall Pass Percentage: {overall_pass_percentage:.2f}% ({total_passed} out of {total_entries})")

    # Calculate and print category-wise results
    for category, counts in category_counts.items():
        category_pass_percentage = (counts["passed"] / counts["total"]) * 100 if counts["total"] > 0 else 0
        print(f"{category} Pass Percentage: {category_pass_percentage:.2f}% ({counts['passed']} out of {counts['total']})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_results.py <input_csv_file_path>")
        sys.exit(1)

    input_csv_file_path = sys.argv[1]
    calculate_results(input_csv_file_path)
