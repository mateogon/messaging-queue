from kafka import KafkaConsumer
from multiprocessing import Process
import threading
import time
import json
def run_consumer(topic,num_consumers, run_time):
    
    print(f"Running {num_consumers} consumers")
    # Function that creates and runs a consumer
    start_time = time.time()
    def run_consumer(consumer_id, run_time):
        try:
            
            consumer = KafkaConsumer(
                topic,
                group_id=None,
                auto_offset_reset='earliest',
                bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Decode bytes to string and parse JSON
            )

            consumer.subscribe([topic])

            for message in consumer:
                current_time = time.time()
                if current_time - start_time > run_time:
                    print(f"Consumer {consumer_id} finishing after {run_time} seconds")
                    break
                message_time = message.value['timestamp']
                    
                delta = current_time - message_time
                if delta < 2:
                    with open(f'consumer_{consumer_id}_data.txt', 'a') as f:
                        f.write(f'{message.value} | {delta}\n')
        except Exception as e:
            print(f"Exception in consumer {consumer_id}: {e}")
        finally:
            print(f"Closing consumer {consumer_id}")
            consumer.close()

            
    # Create and start consumers
    threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=run_consumer, args=(i, run_time))
        t.daemon = True
        t.start()
        print(f"Consumer thread {i} started")
        threads.append(t)

    #return threads

    '''
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
        
        '''
        
if __name__ == "__main__":
    run_consumer(1, 30)