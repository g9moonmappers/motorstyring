from dynamixel_sdk import *

port = PortHandler('/dev/ttyUSB0')
packet = PacketHandler(2.0)

port.openPort()
port.setBaudRate(57600)

print("Scanning for Dynamixel motors...")
for i in range(1, 20):
    model_number, result, error = packet.ping(port, i)
    if result == COMM_SUCCESS:
        print(f"Found motor ID: {i}, model: {model_number}")

port.closePort()
print("Scan complete")
