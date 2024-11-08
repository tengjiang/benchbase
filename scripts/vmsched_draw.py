import os
import csv
import glob
import matplotlib.pyplot as plt
from datetime import datetime

def plot_goodput_vs_latency(config_dir='config/postgres/vmsched'):
    # Set today's date for identifying relevant files
    today = datetime.now().strftime("%Y%m%d")
    summary_files = glob.glob(f"{config_dir}/summary_*_{today}.csv")
    
    # Dictionary to store data for each vm_setting
    data = {}

    # Process each summary CSV file
    for summary_file in summary_files:
        # Extract vm_setting from the filename
        filename_parts = os.path.basename(summary_file).split("_")
        vm_setting = filename_parts[1]

        records = []

        # Read data from the CSV file
        with open(summary_file, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Collect each row's data into a list for sorting
                records.append({
                    "goodput": float(row["Goodput (requests/second)"]),
                    "latency_99th": float(row["99th Percentile Latency (microseconds)"])
                })

        # Sort records by goodput
        records.sort(key=lambda x: x["goodput"])

        # Extract sorted goodput and latency_99th for plotting
        goodput = [record["goodput"] for record in records]
        latency_99th = [record["latency_99th"] for record in records]

        # Store data for plotting
        data[vm_setting] = (goodput, latency_99th)
        print(f"Processed {summary_file} for vm_setting {vm_setting}")

    # Plot each vm_setting as a separate line
    plt.figure(figsize=(10, 6))
    for vm_setting, (goodput, latency_99th) in data.items():
        plt.plot(goodput, latency_99th, marker='o', label=f"VM Setting: {vm_setting}")

    # Label the axes and add title
    plt.xlabel("Goodput (requests/second)")
    plt.ylabel("99th Percentile Latency (microseconds)")
    plt.title("Goodput vs. 99th Percentile Latency")
    plt.legend(title="VM Settings")
    plt.grid(True)

    # Save the plot to a PNG file
    output_file = f"{config_dir}/goodput_vs_latency_{today}.png"
    plt.tight_layout()
    plt.savefig(output_file, format='png')
    print(f"Plot saved as {output_file}")

if __name__ == "__main__":
    plot_goodput_vs_latency()
