#kafka consumer
from kafka import KafkaConsumer
import json

# Create a consumer
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
    print(message.value)  # Print the message value

# Close the consumer
consumer.close()
