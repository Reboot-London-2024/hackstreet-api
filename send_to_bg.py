import serial
from google.cloud import bigquery

# Initialize Google BigQuery client

client = bigquery.Client()

# Configure your Google Cloud project ID and BigQuery dataset ID
project_id = "lbplc-reboot24lon-884"
dataset_id = "hackstreet_data"
table_id = "hackstreet_data_light_sensor"

# Initialize serial connection to Arduino
ser = serial.Serial(
    "/dev/cu.usbmodem142101", 9600
)  # Change 'COM3' to the port where your Arduino is connected

# Define BigQuery table schema
schema = [
    bigquery.SchemaField("sensor_value", "INTEGER"),
    # Add more fields if needed
]

# Create BigQuery table if it doesn't exist
table = bigquery.Table(f"{project_id}.{dataset_id}.{table_id}", schema=schema)
try:
    client.create_table(table)
except:
    pass  # Table already exists

# Read data from Arduino and send it to BigQuery
while True:
    try:
        # Read data from Arduino
        print(ser.readline().strip().decode())
        data = int(ser.readline().strip().decode())
        print("Read data from Arduino:", data)

        # Insert data into BigQuery
        rows_to_insert = [{"sensor_value": data}]
        errors = client.insert_rows_json(table, rows_to_insert)

        if errors:
            print("Encountered errors while inserting rows:", errors)

    except KeyboardInterrupt:
        print("Exiting program")
        break
    except Exception as e:
        print(e)

# Close serial connection
ser.close()
