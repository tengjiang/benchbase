import os
import subprocess
import sys
from datetime import datetime

# Should be in target/benchbase-postgres

def run_benchbase_configs(vm_setting, config_dir='config/postgres/vmsched'):
    # Step 1: Create the database
    create_cmd = [
        "taskset", "-c", "6-9", "java", "-jar", "benchbase.jar",
        "-b", "tpcc", "-c", "config/postgres/sample_vmsched_tpcc_config.xml",
        "--create=true", "--load=true"
    ]
    print("Creating the database...")
    subprocess.run(create_cmd, check=True)
    
    # Step 2: Get today's date for directory organization
    today = datetime.now().strftime("%Y%m%d")
    
    # Step 3: Run each configuration file in the vmsched directory
    for config_file in sorted(os.listdir(config_dir)):
        if config_file.startswith("vmsched_tpcc_") and config_file.endswith(".xml"):
            # Extract the rate from the file name
            config_name = config_file.replace(".xml", "")  # This will be in the format vmsched_tpcc_<rate>
            output_dir = f"{config_dir}/{today}/{vm_setting}/{config_name}"
            os.makedirs(output_dir, exist_ok=True)

            # Run the benchmark with load and execute
            run_cmd = [
                "taskset", "-c", "6-9", "java", "-jar", "benchbase.jar",
                "-b", "tpcc", "-c", f"{config_dir}/{config_file}", "--execute=true", f"--directory={output_dir}"
            ]
            print(f"Running: {config_file} with output in {output_dir}")
            subprocess.run(run_cmd, check=True)

if __name__ == "__main__":
    # Check if vm_setting is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python run_benchbase_configs.py <vm_setting>")
        sys.exit(1)

    vm_setting = sys.argv[1]
    run_benchbase_configs(vm_setting)
