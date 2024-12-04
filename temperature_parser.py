import re
import serial
import csv
from datetime import datetime

# Configure the serial port (update 'COM3' or '/dev/ttyUSB0' based on your system)
SERIAL_PORT = 'COM9'  # Replace with your serial port
BAUD_RATE = 9600  # Adjust to match your device's baud rate
CSV_FILE = '../pythonProject/temperature_log.csv'  # File to save temperature data

# Regex to extract the integer part of the temperature
TEMP_REGEX = r"Temperature:(\d+\.\d{1,2})°C"

def main():
    try:
        # Open the serial connection
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser, \
             open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:

            # Initialize the CSV writer
            csv_writer = csv.writer(csvfile)
            # Write the CSV header
            csv_writer.writerow(["Timestamp", "Temperature"])

            print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...")
            print(f"Logging temperature data to {CSV_FILE}")

            while True:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                # Search for the temperature pattern
                match = re.search(TEMP_REGEX, line)
                if match:
                    # Extract the integer part of the temperature
                    temperature = match.group(1)
                    # Get the current timestamp
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Log the temperature to the CSV
                    csv_writer.writerow([timestamp, temperature])
                    # Print the logged data to the console
                    print(f"{timestamp}, Temperature: {temperature}°C")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
