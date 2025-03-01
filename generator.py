import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 📌 Configuration: Change these as needed
NUM_SERVERS = 1000        # Total number of servers
START_DATE = "2024-01-01" # Start date for data generation (YYYY-MM-DD)
NUM_DAYS = 30             # Number of days to generate data
MISSING_DATA_PROB = 0.1   # Probability that a server has missing data on a given day (10%)

# Convert start date to datetime object
start_datetime = datetime.strptime(START_DATE, "%Y-%m-%d")

# Define the time interval (every 30 seconds)
TIME_INTERVAL = timedelta(seconds=30)

# Create an empty list to store generated data
data = []

# 📌 Generate data for each server
for server_id in range(1, NUM_SERVERS + 1):
    host_name = f"host_{server_id}"
    
    # Generate data for the specified number of days
    for day_offset in range(NUM_DAYS):
        current_day = start_datetime + timedelta(days=day_offset)
        
        # Randomly decide if this server will have missing data for this day
        if random.random() < MISSING_DATA_PROB:
            continue  # Skip this day for this server
        
        # Generate data for the entire day at 30-second intervals
        time = current_day
        while time < (current_day + timedelta(days=1)):
            cpu_used = round(np.random.uniform(10, 90), 2)  # Simulate CPU usage %
            mem_used = round(np.random.uniform(20, 95), 2)  # Simulate Memory usage %
            
            # Append data to the list
            data.append([time, host_name, cpu_used, mem_used])
            
            # Increment time by 30 seconds
            time += TIME_INTERVAL

# 📌 Convert data to a Pandas DataFrame
df = pd.DataFrame(data, columns=["date_time", "host_name", "cpu_used_percent", "mem_used_percent"])

# Save to CSV file
df.to_csv("test_server_metrics.csv", index=False)

print("✅ Test data generated and saved to test_server_metrics.csv")
