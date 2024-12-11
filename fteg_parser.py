"""
DataToCSV.py : Reads and parses inconsistent voltage data from the serial input and writes it to a CSV.
"""

# Importing required libraries
import serial
import csv
from datetime import datetime
import re

def SaveDatatoCSV():
    # Configuration for serial port
    # Adjust 'COM4' to match your system's port
    serialPort = serial.Serial(port="COM10", baudrate=9600, timeout=2)

    # Output CSV file configuration
    output_file = (lambda date: f"fteg_log_{date}.csv") (datetime.now().strftime("%Y%m%d%H%M%S"))
    fieldnames = ["Timestamp", "Voltage (mV)"]

    # Regex to match "Voltage: <value> mV", handling fragmented lines
    VOLTAGE_REGEX = r"Voltage:\s*(-?\d*\.\d+|\d+)\s*mV"

    # Buffer to accumulate partial lines
    buffer = ""

    # Open the CSV file for writing
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        print(f"Listening on {serialPort.port} at {serialPort.baudrate} baud...")
        print(f"Writing data to {output_file}")

        # Looping to process and save the voltage data
        try:
            while True:
                # Check if there is data waiting in the serial buffer
                if serialPort.in_waiting > 0:
                    # Read the serial data as a string
                    serialString = serialPort.read(serialPort.in_waiting).decode("ascii", errors="ignore").strip()
                    buffer += serialString  # Append incoming data to the buffer
                    # print("buffer: " + buffer)
                    # # Split the buffer into lines
                    # lines = buffer.split("\n")
                    # buffer = lines.pop()  # Keep the last (potentially incomplete) line in the buffer

                    # for line in lines:
                    # Clean up and check for a match
                    # line = line.replace("\r", "").strip()
                    match = re.search(VOLTAGE_REGEX, buffer)
                    if match:
                        # Extract voltage value and generate a timestamp
                        voltage = match.group(1)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Write to CSV
                        writer.writerow({"Timestamp": timestamp, "Voltage (mV)": voltage})
                        print(f"{timestamp}, Voltage: {voltage} mV")
                        buffer = ""
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            serialPort.close()
            print("Serial port closed.")

if __name__ == "__main__":
    SaveDatatoCSV()
