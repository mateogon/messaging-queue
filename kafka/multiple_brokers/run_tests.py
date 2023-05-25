import sys
import pandas as pd
import sys
sys.path.append('/home/mateo/Desktop/tarea2_sd')
import get_avg
import k_consumer
import k_producer
import time
import threading
import os
def main():
    try:
        results_df = pd.DataFrame(columns=['num_producers', 'num_consumers', 'delta_t', 'average_latency', 'average_throughput'])
        test_configurations = [(30, 30, 1),(60, 60, 1),(100, 100, 1),(30, 30, 0.1),(30, 30, 0.01)]#,(30, 30, 1),(60, 60, 1),(100, 100, 1),(30, 30, 0.1),(30, 30, 0.01)]
        #test_configurations = [(10, 10, 1), (30, 30, 1), (60, 60, 1),(100, 100, 1),(30, 30, 0.1),(30, 30, 0.01)]  # (num_producers, num_consumers, delta_t)
        topic = "my-topic_3"
        run_time = 12  # seconds
        min_data_size = 5
        max_data_size = 500
        time_between = 6
        # Initialize a dataframe to store the results
        results = {
        'num_producers': [],
        'num_consumers': [],
        'delta_t': [],
        'average_latency': [],
        'average_throughput': []
    }
        for config in test_configurations:
            for i in range(0,3):
                time.sleep(2)
                num_producers, num_consumers, delta_t = config
                print(f"Running test with {num_producers} producers, {num_consumers} consumers and {delta_t} delta_t")
                print("Starting consumer threads")
                #consumer_thread = k_consumer.run_consumer(num_consumers, run_time)
                consumer_thread = threading.Thread(target=k_consumer.run_consumer, args=(topic,num_producers, run_time+time_between+2))
                consumer_thread.start()
                time.sleep(time_between-2)
                print("Starting producer thread")
                producer_thread = threading.Thread(target=k_producer.run_producer, args=(topic,num_producers, run_time, delta_t))
                producer_thread.start()
                print("Waiting for threads to finish")
                time.sleep(run_time+10)
                producer_thread.join()
                print("Producer thread finished")
                consumer_thread.join()
                #for t in consumer_threads:
                #    t.join()
                print("Consumer threads finished")
                
                average_latency, average_throughput = get_avg.calculate_average()
                print(f"Average Latency: {average_latency}, Average Throughput: {average_throughput}")
                # Append the result to the dataframe
                # Append to results
                results['num_producers'].append(num_producers)
                results['num_consumers'].append(num_consumers)
                results['delta_t'].append(delta_t)
                results['average_latency'].append(average_latency)
                results['average_throughput'].append(average_throughput)

            # Save the dataframe to a CSV file
            results_df = pd.DataFrame(results)
            results_df.to_csv(os.curdir+'test_results.csv', index=False)

            print("Test results saved to 'test_results.csv'.")
    except Exception as e:
        print(f"Exception in main: {e}")
        

if __name__ == "__main__":
    main()
