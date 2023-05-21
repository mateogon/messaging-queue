# Import the necessary libraries
import time

from kafka import KafkaProducer, KafkaConsumer

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: x.encode('utf-8')
)

# Create a Kafka consumer
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Produce messages
for i in range(10):
    producer.send('my-topic', i)
    time.sleep(1)

# Consume messages
for message in consumer:
    print(message.value)

# Close the producer and consumer
producer.close()
consumer.close()