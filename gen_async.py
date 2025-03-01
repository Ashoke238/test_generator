import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import multiprocessing

# 📌 Configuration
NUM_SERVERS = 1000         # Total number of servers
START_DATE = "2024-01-01"  # Start date for data generation (YYYY-MM-DD)
NUM_DAYS = 30              # Number of days to generate data
MISSING_DATA_PROB = 0.1    # Probability that a server has missing data on a given day (10%)
TIME_INTERVAL = timedelta(seconds=30)  # Data collection frequency

# Convert start date to datetime object
start_datetime = datetime.strptime(START_DATE, "%Y-%m-%d")

def generate_server_data(server_id):
    """Generates synthetic data for a single server across multiple days."""
    host_name = f"host_{server_id}"
    data = []

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

            # Append generated row
            data.append([time, host_name, cpu_used, mem_used])

            # Increment time
            time += TIME_INTERVAL

    return data

def parallel_data_generation():
    """Uses multiprocessing to generate data for all servers in parallel."""
    num_cores = multiprocessing.cpu_count()  # Get number of available CPU cores
    print(f"⚡ Using {num_cores} CPU cores for parallel processing...")

    # Create a pool of workers to process servers in parallel
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(generate_server_data, range(1, NUM_SERVERS + 1))

    # Flatten the list of lists into a single list
    all_data = [row for server_data in results for row in server_data]

    # Convert to Pandas DataFrame
    df = pd.DataFrame(all_data, columns=["date_time", "host_name", "cpu_used_percent", "mem_used_percent"])

    # Save to CSV file
    df.to_csv("test_server_metrics.csv", index=False)

    print("✅ Test data generated and saved to test_server_metrics.csv")

if __name__ == "__main__":
    parallel_data_generation()
