#rabbit consumer
import pika
import json

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
    print(f" [x] Received {message}")

# Set the callback function
channel.basic_consume(queue='iot_data', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

# Start consuming
channel.start_consuming()
