#kafka producer

import json
import time
import random
import string
from kafka import KafkaProducer
from threading import Thread

# Set the number of devices
n = 10

# Set the delta time in seconds
delta_t = 2

# Set the running time in seconds
running_time = 60

# Set the range for the random data size
min_data_size = 5
max_data_size = 15

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Create a shared variable for the threads to know when to stop
stop_threads = False

def simulate_device(device_id):
    global stop_threads
    while not stop_threads:
        # Generate random data of random size
        data_size = random.randint(min_data_size, max_data_size)
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
        producer.send('my-topic', message)

        # Wait for delta time before sending the next message
        time.sleep(delta_t)

# Create and start a thread for each device
for i in range(n):
    Thread(target=simulate_device, args=(i,)).start()

# Let the threads run for the specified running time
time.sleep(running_time)

# After the running time has passed, signal the threads to stop
stop_threads = True
