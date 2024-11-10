README for Github:
#### Project Overview
Provide a brief summary of the project, objectives, and expected outcomes.

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
export TRANSFORMERS_CACHE=/mnt/extra-disk/huggingface_cache
export HF_HOME=/mnt/extra-disk/huggingface_home

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

7. **Run the Script**:
   ```bash
   cd semcoder/scripts
python run.py ../datasets/<dataset_file> ../results/<results_file>
   ```

**Guide 2: Without Using an External Disk**

1. **Install requirements Locally**:
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

4. **Run the Script**:
   ```bash
    cd semcoder/scripts
    python run.py ../datasets/<dataset_file> ../results/<results_file>
   ```
