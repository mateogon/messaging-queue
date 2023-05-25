from kafka import KafkaAdminClient
from kafka.admin import NewTopic
admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
topic_name = "my-topic_4"
num_partitions = 5
replication_factor = 1

topic_list = admin_client.list_topics()
if topic_name not in topic_list:
    topic = NewTopic(
        name=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )

    admin_client.create_topics(new_topics=[topic], validate_only=False)
else:
    print(f"Topic '{topic_name}' already exists.")