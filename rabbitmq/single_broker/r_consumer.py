from multiprocessing import Process
import pika
import json
import time

# Function that creates and runs a consumer
def run_consumer(consumer_id):
    # Define your RabbitMQ connection parameters and credentials
    credentials = pika.PlainCredentials('user', 'bitnami')
    parameters = pika.ConnectionParameters('localhost', credentials=credentials)

    # Connect to the RabbitMQ server
    connection = pika.BlockingConnection(parameters)

    # Create a new channel
    channel = connection.channel()

    # Declare the queue from which we're going to consume
    channel.queue_declare(queue='iot_data')

    # Define the callback function that's going to process the messages
    def callback(ch, method, properties, body):
        message = json.loads(body)
        current_time = time.time()  # Get the current time in seconds
        message_time = message['timestamp']  # Get the message timestamp

        # Calculate the delta for latency
        delta = current_time - message_time  # Calculate the delta
        if delta < 30:
            with open(f'consumer_{consumer_id}_latency.txt', 'a') as f:
                f.write(f'{delta}\n')  # Write the delta to the file

    # Set the callback function
    channel.basic_consume(queue='iot_data', on_message_callback=callback, auto_ack=True)

    print(f'Consumer {consumer_id} is waiting for messages. To exit press CTRL+C')

    # Start consuming
    channel.start_consuming()

# Number of consumers
num_consumers = 10

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
