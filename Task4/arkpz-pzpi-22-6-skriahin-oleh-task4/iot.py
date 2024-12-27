import random
import time
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from iot_config import API_URL, SENSORS_API_URL, HEADERS, NORMAL_RANGES, DANGEROUS_RANGES, DANGEROUS_PROBABILITY

def fetch_sensors():
    """
    Fetch the list of sensors from the API.
    """
    try:
        response = requests.get(SENSORS_API_URL, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[{datetime.now()}] Failed to fetch sensor data: {response.json()}")
            return []
    except requests.RequestException as e:
        print(f"[{datetime.now()}] Error fetching sensor data: {e}")
        return []

def generate_sensor_data(sensor_type):
    """
    Generate random data for a sensor with a probability of dangerous values.
    """
    is_dangerous = random.random() < DANGEROUS_PROBABILITY
    if is_dangerous:
        return random.uniform(*DANGEROUS_RANGES[sensor_type])
    return random.uniform(*NORMAL_RANGES[sensor_type])

def calculate_average(sensor_type, sensors):
    """
    Calculate the average value for a given sensor type based on all sensors of the same type.
    """
    values = [generate_sensor_data(s['type']) for s in sensors if s['type'] == sensor_type]
    return sum(values) / len(values) if values else None

def check_adjacent_sensors(sensor, sensors):
    """
    Check the adjacent sensors of the same type for normal values.
    """
    sensor_type = sensor['type']
    adjacent_sensors = [s for s in sensors if s['type'] == sensor_type and s['id'] != sensor['id']]
    normal_values = [NORMAL_RANGES[sensor_type][0] <= generate_sensor_data(sensor_type) <= NORMAL_RANGES[sensor_type][1] for s in adjacent_sensors]
    return all(normal_values)

def send_data_to_server(sensor, sensors):
    """
    Send sensor data to the server via API with additional fault detection logic.
    """
    sensor_id = sensor["id"]
    sensor_type = sensor["type"]
    value = generate_sensor_data(sensor_type)

    # Calculate the average value for the sensor type
    average_value = calculate_average(sensor_type, sensors)
    if average_value and abs(value - average_value) / average_value > 0.3:  # 30% deviation
        if check_adjacent_sensors(sensor, sensors):
            print(f"[{datetime.now()}] WARNING: Sensor {sensor_id} might be faulty. Value: {value:.2f}, Average: {average_value:.2f}")

    payload = {
        "sensor_id": sensor_id,
        "value": value
    }
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        if response.status_code == 201:
            print(f"[{datetime.now()}] Log created successfully for sensor {sensor_id} with value {value:.2f}")
        else:
            print(f"[{datetime.now()}] Failed to create log for sensor {sensor_id}: {response.json()}")
    except requests.RequestException as e:
        print(f"[{datetime.now()}] Error sending data to server for sensor {sensor_id}: {e}")

def simulate_sensors():
    """
    Simulate data generation and transmission for all sensors.
    """
    while True:
        sensors = fetch_sensors()
        if sensors:
            print(f"[{datetime.now()}] Retrieved {len(sensors)} sensors. Starting data generation...")
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda s: send_data_to_server(s, sensors), sensors)
        else:
            print(f"[{datetime.now()}] No sensors found or failed to fetch sensors.")
        time.sleep(40)  # Wait 40 seconds before the next cycle

if __name__ == "__main__":
    print("Starting IoT sensor simulation...")
    simulate_sensors()