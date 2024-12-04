import pandas as pd

def combine_csvs(voltage_csv, temperature_csv, output_csv):
    """
    Combines voltage and temperature CSV files based on timestamps.

    Parameters:
    - voltage_csv (str): Path to the voltage CSV file.
    - temperature_csv (str): Path to the temperature CSV file.
    - output_csv (str): Path to save the combined CSV file.
    """
    # Load the CSV files
    voltage_data = pd.read_csv(voltage_csv)
    temperature_data = pd.read_csv(temperature_csv)

    # Merge the data on the 'Timestamp' column
    combined_data = pd.merge(voltage_data, temperature_data, on="Timestamp", how="inner")

    # Sort by Timestamp to ensure chronological order
    combined_data.sort_values(by="Timestamp", inplace=True)

    # Save the combined data to a new CSV file
    combined_data.to_csv(output_csv, index=False)

    print(f"Combined data saved to {output_csv}")

if __name__ == "__main__":
    # Specify the input and output file paths
    voltage_csv = "fteg_data.csv"
    temperature_csv = "temperature_log.csv"
    output_csv = "combined_data2.csv"

    # Combine the CSV files
    combine_csvs(voltage_csv, temperature_csv, output_csv)
