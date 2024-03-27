import random
import time
import requests
import json
from datetime import datetime
import pytz

# Firebase Realtime Database URL
database_url = "https://siddhi-project-67c6e-default-rtdb.firebaseio.com/"

# Function to generate random data
def generate_random_data():
    ist = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S') # Changed ':' to '-'
    return {
        'K': round(random.uniform(60, 80), 2),  # Adjusted range for Potassium (K)
        'N': round(random.uniform(5, 10), 2),   # Adjusted range for Nitrogen (N)
        'P': round(random.uniform(20, 40), 2),  # Adjusted range for Phosphorus (P)
        'Soil Moisture': round(random.uniform(0, 100), 2),  # Adjusted range for Soil Moisture
        'ec': round(random.uniform(80, 90), 2),  # Adjusted range for Electrical Conductivity (ec)
        'humidity': round(random.uniform(50, 80), 2),  # Adjusted range for Humidity
        'ph': round(random.uniform(6, 7.5), 2),  # Adjusted range for pH
        'timestamp': timestamp
    }

# Function to send data to Firebase
def send_data_to_firebase(data, node):
    try:
        response = requests.put(database_url + f'{node}/{data["timestamp"]}.json', data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"{node} data sent:", data)
    except Exception as e:
        print(f"An error occurred while sending {node} data:", e)

# Main loop to continuously send random data
while True:
    try:
        data = generate_random_data()
        
        # Send data to Realtime and Past nodes separately
        send_data_to_firebase(data, "realtime")
        send_data_to_firebase(data, "past")
        
        time.sleep(5)  # Send data every 5 seconds
    except Exception as e:
        print("An error occurred:", e)
        # Handle the error, maybe log it or try to recover gracefully
