from kafka import KafkaAdminClient

# Create a client
client = KafkaAdminClient(bootstrap_servers='localhost:9092')

# Create the topic
client.create_topic('my-topic', 1, 1)