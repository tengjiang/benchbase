import xml.etree.ElementTree as ET
import os

def generate_configs(start_rate, end_rate, interval, template_file='sample_vmsched_tpcc_config.xml', output_dir='vmsched'):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse the template XML file
    tree = ET.parse(template_file)
    root = tree.getroot()

    # Iterate over the range of rates
    for rate in range(start_rate, end_rate + 1, interval):
        # Update the rate in the XML structure
        for work in root.findall("./works/work/rate"):
            work.text = str(rate)

        # Define the output filename based on the rate
        output_filename = f"{output_dir}/vmsched_tpcc_{rate}.xml"
        
        # Write the modified XML to a new file
        tree.write(output_filename, encoding="utf-8", xml_declaration=True)
        print(f"Generated: {output_filename}")

# Parameters for generating configurations
start_rate = 250   # Replace with desired start rate
end_rate = 2500    # Replace with desired end rate
interval = 250     # Replace with desired interval

generate_configs(start_rate, end_rate, interval)
