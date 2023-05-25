import glob
import numpy as np
import os
import sys

def calculate_average():
    #print("Calculating average...")
    # Use glob to get all the filenames that match the pattern
    filenames = glob.glob('consumer_*_data.txt')
    #print(f"Found {len(filenames)} files.")

    # Initialize lists to store all numbers and throughput
    all_numbers = []
    throughputs = []

    # Loop over the filenames
    for filename in filenames:
        #print(f"Processing file: {filename}")
        # Open the file
        with open(filename, 'r') as f:
            # Read the lines in the file
            lines = f.readlines()
            #print(f"Found {len(lines)} lines in the file.")

            # Loop over the lines
            for line in lines:
                # Parse the message and delta time
                message, delta_str = line.strip().split(' | ')
                delta = float(delta_str)
                
                # Append the delta time to the list
                all_numbers.append(delta)

                # Calculate the size of the message in bytes
                message_size = sys.getsizeof(message)
                #print(f"Message size: {message_size} bytes.")
                
                # Calculate the throughput and append it to the list
                # Please note that we convert delta to seconds and message_size to kilobytes
                # If you want to use other units, you need to adjust the conversion
                throughput = message_size / 1024 / delta  # KB/s
                throughputs.append(throughput)
                #print(f"Throughput: {throughput} KB/s.")

        # Delete the file after reading
        #print(f"Deleting file: {filename}")
        os.remove(filename)

    # Compute the averages
    #print("Calculating averages...")
    average_latency = np.mean(all_numbers)
    average_throughput = np.mean(throughputs)
    

    return average_latency, average_throughput
