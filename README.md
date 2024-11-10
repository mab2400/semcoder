Mia Bramel
11/9/24
Midterm Report - Code Submission

#### Project Overview
[SemCoder Ablation Study] Programming by examples. How useful are the input/output examples
described in the prompt?
- What will happen if we remove those examples from the HumanEval prompt, how much will the
performance drop?
- Is the execution training increasing/decreasing the dependence on these I/O examples?

#### Requirements
- 1 GPU
- At least 200 GB of disk space
- **Software Requirements**:
  - Python
  - Transformers
  - PyTorch

---

### Running the Code on a Clean Environment

#### 1. Prerequisites
Ensure you have access to:
- A GPU-enabled virtual machine or local system
- Sufficient disk space (~ 200 GB for installing packages)

#### 2. Installation Instructions

**Guide 1: Using an External Disk That Needs to Be Mounted**

1. **Mount the External Disk**:
   ```bash
   lsblk
   sudo mkdir -p /mnt/extra-disk
   sudo mount /dev/sdb /mnt/extra-disk
   sudo mkdir /mnt/extra-disk/python_packages
   sudo chown -R $(whoami):$(whoami) /mnt/extra-disk/python_packages
   chmod -R 775 /mnt/extra-disk/python_packages
   export PYTHONPATH=/mnt/extra-disk/python_packages:$PYTHONPATH
   ```

2. Set cache and install directories:
   ```bash
    export TRANSFORMERS_CACHE=/mnt/extra-disk/huggingface_cache
    export HF_HOME=/mnt/extra-disk/huggingface_home
    ```

3. **Create a Temporary Directory**:
   ```bash
   mkdir -p /mnt/extra-disk/tmp
   ```

4. **Install Required Python Packages**:
   ```bash
    TMPDIR=/mnt/extra-disk/tmp pip install -r requirements.txt --target=/mnt/extra-disk/python_packages --no-cache-dir
   ```

5. **Install Git**:
   ```bash
   sudo apt install git -y
   ```

6. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/semcoder.git
   ```

**Guide 2: Without Using an External Disk**

1. **Install requirements locally**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Install Git**:
   ```bash
   sudo apt install git -y
   ```

3. **Clone the Repository**:
   ```bash
   git clone https://github.com/mab2400/semcoder.git
   ```

# Project Scripts Overview

## Step 1: `run.py <input_file> <output_file>`
This script runs SemCoder on a given dataset (either control or ablation) and executes the test cases on the generated code. It produces an output CSV file with the generated code and the pass/fail results.

### Functionality:
- Load dataset
- Run SemCoder on each example
- Execute provided test cases on the generated code
- Generate a CSV output with columns:
  - `entry_point`
  - `prompt`
  - `test_cases`
  - `generated_code`
  - `all_tests_passed`
  - `category`

### Usage:
```bash
python run.py <input_file> <output_file>
```

## (Optional Debugging Step:) `run_single_example.py <entry_point>`
A script that runs SemCoder and executes test cases on a single example from either dataset. Useful for testing or debugging individual entries.

### Functionality:
- Take an example as input via the command line
- Run SemCoder on the given example
- Execute test cases and display results
- Display the result in the terminal

### Usage:
```bash
python run_single_example.py <entry_point>
```

## Step 2: `calculate_results.py <input_file>`
A script that calculates the overall pass percentage and category breakdown of pass rates for the datasets (both "control" and "ablation").

### Functionality:
- Load the CSV file containing pass/fail results and categories
- Calculate the overall success rate
- Compute category-wise success rates
- Prints a report

### Usage:
```bash
python calculate_results.py <results_csv_file>
```

### Important Note: 
While examining the generated code, I noticed that SemCoder will sometimes generate test cases
for a prompt if it has not met the max_token limit yet. Since I only use the Humaneval-provided
test cases for my evaluations, these extra SemCoder-generated test cases are not needed (and 
actually created many errors during evaluation because often the generated test cases would 
get cut off at the max_token limit and leave an unfinished bit of code). To maintain consistency
and accuracy in my evaluations, I decided to hand-remove any extraneous generations from the 
'generated_code' section of the CSV output file. If you do NOT choose to hand-remove any part 
of the generated code, be aware that your performance percentages might appear LOWER than the 
values I reported.
