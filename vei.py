from dynamixel_sdk import *

port = PortHandler('COM3')  # Change COM3 to whatever port your U2D2 is on
packet = PacketHandler(2.0)

if not port.openPort():
    print("Failed to open port!")
    exit()

if not port.setBaudRate(57600):
    print("Failed to set baudrate!")
    exit()

print("Port opened successfully!")

# Set velocity mode and enable torque for all 6
for id in [1,2,3,4,5,6]:
    packet.write1ByteTxRx(port, id, 11, 1)  # velocity mode
    packet.write1ByteTxRx(port, id, 64, 1)  # torque on
    print(f"Motor {id} ready")

# Spin all at slow speed
for id in [1,3,5]:  # right side
    packet.write4ByteTxRx(port, id, 104, 50)
for id in [2,4,6]:  # left side
    packet.write4ByteTxRx(port, id, 104, 50)

print("All motors spinning - watch which way they turn!")
input("Press Enter to stop...")

# Stop and disable torque
for id in [1,2,3,4,5,6]:
    packet.write4ByteTxRx(port, id, 104, 0)
    packet.write1ByteTxRx(port, id, 64, 0)

port.closePort()
print("Done!")
