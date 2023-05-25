from kafka import KafkaConsumer
from multiprocessing import Process
import time
import json

# Function that creates and runs a consumer
def run_consumer(consumer_id):
    consumer = KafkaConsumer(
        'my-topic',
        group_id=None,
        auto_offset_reset='earliest',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Decode bytes to string and parse JSON
    )

    # Subscribe to the topic
    consumer.subscribe(['my-topic'])

    # Consume messages
    for message in consumer:
        current_time = time.time()  # Get the current time in seconds
        message_time = message.value['timestamp']  # Get the message timestamp
        
        # Calculate the delta para latencia
        delta = current_time - message_time  # Calculate the delta
        if delta < 30:
            with open(f'consumer_{consumer_id}_latency.txt', 'a') as f:
                f.write(f'{delta}\n')  # Write the message value and delta to the file

    # Close the consumer
    consumer.close()

# Number of consumers
num_consumers = 30

# Create and start consumers
processes = []
for i in range(num_consumers):
    p = Process(target=run_consumer, args=(i,))
    p.start()
    processes.append(p)

def terminate_processes(processes):
    # Terminate all child processes
    for p in processes:
        p.terminate()
        p.join()
# Wait for all consumers to finish
try:
    # Wait for all child processes to finish
    for p in processes:
        p.join()
except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
    print("KeyboardInterrupt detected. Terminating processes...")
    terminate_processes(processes)