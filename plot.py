import pandas as pd
import matplotlib.pyplot as plt

# Assuming your data is in a CSV file called 'data.csv'
data = pd.read_csv('test_results copy.csv')
print(data.head())
plt.figure(figsize=(10, 8))

# Create a scatter plot with average_latency and average_throughput
scatter = plt.scatter((data['num_consumers']+data['num_producers']), data['average_latency'], cmap='jet')

# Add a color bar and labels
plt.colorbar(scatter, label='delta_t')
plt.xlabel('Number of Producers+Consumers')
plt.ylabel('Average Latency')
plt.title('Average Latency by Number of Producers+Consumers and constant delta_t')

plt.show()
