import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MinuteLocator
from scipy.stats import norm

# Load dataset (replace with your own CSV file path)
data = 'data.csv'
df = pd.read_csv(data)

# Convert 'time(sec)' column to datetime
df['time(sec)'] = pd.to_datetime(df['time(sec)'])

# Filter the data for the specified time range
start_time = pd.Timestamp('09:00:00')
end_time = pd.Timestamp('23:30:00')
filtered_df = df[
    (df['time(sec)'].dt.time >= start_time.time()) &
    (df['time(sec)'].dt.time <= end_time.time())
].copy()

# Calculate the ratio of 'live_traffic(sec)' to 'normal_traffic(sec)'
filtered_df['ratio'] = filtered_df['live_traffic(sec)'] / filtered_df['normal_traffic(sec)']

# Plot histograms
plt.hist(filtered_df['ratio'], bins=100)
plt.title("Traffic Ratio Distribution")
plt.show()

plt.hist(np.log(filtered_df['ratio']) + 3, bins=100)
plt.title("Log-Transformed Traffic Ratio Distribution")
plt.show()

# Estimate Gaussian distribution
def estimate_gaussian(X): 
    m = len(X)
    mu = 1 / m * np.sum(X, axis=0)
    var = 1 / m * np.sum((X - mu) ** 2, axis=0)        
    return mu, var

X1 = np.log(filtered_df['ratio']) + 3
m1, v1 = estimate_gaussian(X1)

print("Mean:", m1, "Variance:", v1)

pdf_X1 = norm.pdf(X1, m1, np.sqrt(v1))
pdf_X1_normalized = pdf_X1 / np.sum(pdf_X1)

print("Normalized PDF Sum:", np.sum(pdf_X1_normalized))

# Find anomalies
anomaly_indices = [i for i, j in enumerate(pdf_X1) if j < 0.8]
print("Number of anomalies detected:", len(anomaly_indices))

# Helper function to extract row values
def get_row_value(row_number):
    if row_number in df.index:  
        item = df.iloc[row_number].tolist() 
        return [str(i) if isinstance(i, pd.Timestamp) else i for i in item]
    else:
        return None
      
# Collect anomaly data
anomaly_data = []
for row in anomaly_indices:
    value = get_row_value(row)
    anomaly_data.append(value)
anomaly_data = np.array(anomaly_data)

# Graph function for visualizing anomalies
def graph(i, anomaly_data):
    file_path = f"Apr{i}_2.xlsx"  # replace with your dataset path
    df = pd.read_excel(file_path)

    df['time(sec)'] = pd.to_datetime(df['time(sec)'])
    filtered_df = df[
        (df['time(sec)'].dt.time >= start_time.time()) &
        (df['time(sec)'].dt.time <= end_time.time())
    ].copy()
    filtered_df['ratio'] = filtered_df['live_traffic(sec)'] / filtered_df['normal_traffic(sec)']

    anomaly_df = pd.DataFrame(
        anomaly_data,
        columns=['normal_traffic(sec)', 'live_traffic(sec)', 'time(sec)', 'length(m)', 'date']
    )
    anomaly_df['time(sec)'] = pd.to_datetime(anomaly_df['time(sec)'])
    anomaly_df['live_traffic(sec)'] = pd.to_numeric(anomaly_df['live_traffic(sec)'])
    anomaly_df['normal_traffic(sec)'] = pd.to_numeric(anomaly_df['normal_traffic(sec)'])

    plt.figure(figsize=(16, 8))
    date_groups = filtered_df.groupby('date')
    for date, group in date_groups:
        plt.plot(group['time(sec)'], group['ratio'], label=date)

        anomalies = anomaly_df[anomaly_df['date'] == date]
        if not anomalies.empty:
            plt.scatter(
                anomalies['time(sec)'],
                anomalies['live_traffic(sec)'] / anomalies['normal_traffic(sec)'],
                color='red', marker='x', s=50
            )

    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(MinuteLocator(interval=30))
    plt.xticks(rotation=45)
    plt.xlabel('Time (sec)')
    plt.ylabel('Traffic Ratio (Live / Normal)')
    plt.title('Traffic Ratio Analysis with Anomaly Detection')
    plt.legend(title='Date', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Example call (replace "17" with the correct dataset day)
graph(17, anomaly_data)
