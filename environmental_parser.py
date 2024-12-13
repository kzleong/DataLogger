import csv
import re
import time
from datetime import datetime


class SerialDataLogger:
    def __init__(self, csv_file):
        """
        Initializes the logger with a CSV file.
        """
        self.csv_file = csv_file
        self.data = {
            "Timestamp": None,
            "Sound Level (mV)": None,
            "Temperature (°C)": None,
            "Humidity (%)": None,
            "AQI UBA": None,
            "AQI ScioSense": None,
            "TVOC": None,
            "ECO2": None,
            "RS0": None,
            "RS1": None,
            "RS2": None,
            "RS3": None,
        }

        # Write CSV headers if the file is empty
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.data.keys())
            if file.tell() == 0:  # File is empty
                writer.writeheader()

    def log_data(self):
        """
        Logs the current data dictionary to the CSV file.
        """
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.data.keys())
            writer.writerow(self.data)

    def parse_line(self, line):
        """
        Parses a single line of serial data and updates the data dictionary.
        """
        # Match timestamped sound sensor data
        sound_match = re.search(
            r"Published Sound Level \(mV\):\s*(-?\d+(?:\.\d+)?)", line
        )
        if sound_match:
            self.data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.data["Sound Level (mV)"] = float(sound_match.group(1))

        # Match temperature and humidity data
        temp_humidity_match = re.search(
            r"Temp:\s*(-?\d+(?:\.\d+)?)\s*°C, Humidity:\s*(-?\d+(?:\.\d+)?)\s*%",
            line,
        )
        if temp_humidity_match:
            self.data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.data["Temperature (°C)"] = float(temp_humidity_match.group(1))
            self.data["Humidity (%)"] = float(temp_humidity_match.group(2))

        # Match AQI, TVOC, and ECO2 data
        aqi_match = re.search(
            r"AQI UBA:\s*(\d+),\s*AQI ScioSense:\s*(\d+),\s*TVOC:\s*(\d+),\s*ECO2:\s*(\d+),\s*RS0:\s*(\d+),\s*RS1:\s*(\d+),\s*RS2:\s*(\d+),\s*RS3:\s*(\d+)",
            line,
        )
        if aqi_match:
            self.data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.data["AQI UBA"] = int(aqi_match.group(1))
            self.data["AQI ScioSense"] = int(aqi_match.group(2))
            self.data["TVOC"] = int(aqi_match.group(3))
            self.data["ECO2"] = int(aqi_match.group(4))
            self.data["RS0"] = int(aqi_match.group(5))
            self.data["RS1"] = int(aqi_match.group(6))
            self.data["RS2"] = int(aqi_match.group(7))
            self.data["RS3"] = int(aqi_match.group(8))

        # Log the data after every parsed line
        self.log_data()


if __name__ == "__main__":
    # Example usage
    logger = SerialDataLogger("sensor_data.csv")

    # Simulating serial input
    simulated_serial_output = [
        "I (7927) ENS: [device_f0f5bd06f5a0] AQI UBA: 1, AQI ScioSense: 96, TVOC: 62, ECO2: 591, RS0: 1, RS1: 1, RS2: 1, RS3: 41136",
        "I (7928) SoundSensor: [device_f0f5bd06f5a0] Published Sound Level (mV): 361.03",
        "I (9058) ENS: [device_f0f5bd06f5a0] Temp: 26.45 °C, Humidity: 33.02 %",
        "I (8234) SoundSensor: [device_f0f5bd06f5a0] Published Sound Level (mV): 696.26",
    ]

    for line in simulated_serial_output:
        logger.parse_line(line)
        time.sleep(0.1)  # Simulating delay between lines
