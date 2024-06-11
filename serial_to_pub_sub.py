import serial
import time
from google.cloud import pubsub_v1

# Serial setup
serial_port = "/dev/cu.usbmodem142101"  # Replace with your actual serial port
baud_rate = 9600

# GCP Pub/Sub setup
project_id = "your_project_id"
topic_id = "your_topic_id"

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)  # Wait for the connection to establish

# Initialize Pub/Sub publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()
            print(f"Sensor Value: {line}")
            data = line.encode("utf-8")
            future = publisher.publish(topic_path, data)
            print(f"Published message ID: {future.result()}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)
