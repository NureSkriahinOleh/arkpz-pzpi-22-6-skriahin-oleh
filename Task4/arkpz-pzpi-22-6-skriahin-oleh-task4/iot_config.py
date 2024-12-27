# iot_config.py
"""
Configuration module for the IoT application.
"""

API_URL = "https://smartshield.onrender.com/api/v1/sensor/sensors/logs/create/"  # API endpoint for sending data
SENSORS_API_URL = "https://smartshield.onrender.com/api/v1/sensor/sensors/"  # API endpoint for fetching sensors
HEADERS = {"Content-Type": "application/json"}

NORMAL_RANGES = {
    "humidity": (30, 70),      # Percentage
    "temperature": (20, 45),  # Degrees Celsius
    "gas": (10, 35),          # ppm
}

DANGEROUS_RANGES = {
    "humidity": (10, 20),      # Low humidity
    "temperature": (50, 70),   # High temperature
    "gas": (35, 70),           # High gas concentration
}

DANGEROUS_PROBABILITY = 0.1  # Probability of generating dangerous values