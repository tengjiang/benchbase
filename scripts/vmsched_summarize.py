import os
import sys
import json
import csv
from datetime import datetime

def summarize_results(vm_setting, config_dir='config/postgres/vmsched'):
    # Set the date-based path
    today = datetime.now().strftime("%Y%m%d")
    base_dir = f"{config_dir}/{today}/{vm_setting}"
    
    # Prepare the CSV file
    csv_filename = f"{config_dir}/summary_{vm_setting}_{today}.csv"
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(["Rate", "Throughput (requests/second)", "Goodput (requests/second)", 
                         "Median Latency (microseconds)", "99th Percentile Latency (microseconds)"])

        # Traverse each config setting directory and process .summary.json files
        for config_name in sorted(os.listdir(base_dir)):
            config_path = os.path.join(base_dir, config_name)
            
            # Look for the .summary.json file in the directory
            summary_file = None
            for file_name in os.listdir(config_path):
                if file_name.endswith(".summary.json"):
                    summary_file = os.path.join(config_path, file_name)
                    break
            
            if summary_file and os.path.isfile(summary_file):
                # Read and parse the .summary.json file
                with open(summary_file, 'r') as f:
                    data = json.load(f)
                
                # Extract required values
                rate = config_name.split('_')[-1]  # Extract rate from config name
                throughput = data.get("Throughput (requests/second)", 0)
                goodput = data.get("Goodput (requests/second)", 0)
                median_latency = data.get("Latency Distribution", {}).get("Median Latency (microseconds)", 0)
                latency_99th = data.get("Latency Distribution", {}).get("99th Percentile Latency (microseconds)", 0)
                
                # Write the data to CSV
                writer.writerow([rate, throughput, goodput, median_latency, latency_99th])
                print(f"Processed: {summary_file}")

    print(f"Summary CSV generated: {csv_filename}")

if __name__ == "__main__":
    # Check if vm_setting is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python summarize_results.py <vm_setting>")
        sys.exit(1)

    vm_setting = sys.argv[1]
    summarize_results(vm_setting)
