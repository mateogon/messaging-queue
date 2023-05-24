#rabbit producer

import pika
import json
import time
import random
import string
from threading import Thread, Lock
from math import exp
# Set the number of devices
n = 10

# Set the delta time in seconds
delta_t = 2

# Set the running time in seconds
running_time = 60

# Set min and max data size
min_data_size = 5
max_data_size = 500

# Create a RabbitMQ connection
credentials = pika.PlainCredentials('user', 'bitnami')
parameters = pika.ConnectionParameters('localhost', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='iot_data')

# Create a shared variable for the threads to know when to stop
stop_threads = False

# Create a lock object to synchronize threads
lock = Lock()

def simulate_device(device_id, data_size):
    global stop_threads
    while not stop_threads:
        # Generate random data
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=data_size))

        # Create the message
        message = {
            "timestamp": time.time(),
            "value": {
                "device_id": device_id,
                "data": data
            }
        }

        # Send the message
        print(f"Device {device_id} is producing message: {message}")
        with lock:
            channel.basic_publish(exchange='', routing_key='iot_data', body=json.dumps(message))

        # Wait for delta time before sending the next message
        time.sleep(delta_t)

# Create and start a thread for each device
for i in range(n):
    # Calculate the data size for the device
    m = i+1
    data_size = round(min((min_data_size + (max_data_size - min_data_size) * (1 - exp(-i / m))) / m, max_data_size))

    device = Thread(target=simulate_device, args=(i,data_size))
    # Set the thread as a daemon so it will be terminated once the main thread is terminated
    device.daemon = True
    device.start()
    
# Let the threads run for the specified running time
time.sleep(running_time)

# After the running time has passed, signal the threads to stop
stop_threads = True

# Close the RabbitMQ connection
connection.close()
