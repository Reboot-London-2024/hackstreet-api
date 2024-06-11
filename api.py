from flask import Flask, request
from flask_cors import CORS, cross_origin
import serial

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

# Configure the serial port (adjust as per your setup)
arduino_port = "/dev/cu.usbmodem142101"  # Linux
# arduino_port = 'COM3'  # Windows
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate)


@app.route("/display", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def display():
    username = request.args.get("username")
    task = request.args.get("task")

    if username and task:
        data = f"display;{username};{task}\n"
        ser.write(data.encode())

        return "Displayed on LCD", 200
    else:
        return "Missing parameters", 400


@app.route("/rotate_servo", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def rotate_servo():
    data = "rotate_servo;\n"
    ser.write(data.encode())

    return "Servo rotated for 10 seconds", 200


@app.route("/trigger_led", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def trigger_led():
    data = "trigger_led;\n"
    ser.write(data.encode())

    return "LED triggered", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
