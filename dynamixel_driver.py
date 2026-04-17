import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from dynamixel_sdk import *

DEVICE = '/dev/ttyUSB0'
BAUDRATE = 57600
LEFT_ID = 1
RIGHT_ID = 2

MODE_ADDR = 11
TORQUE_ADDR = 64
VELOCITY_ADDR = 104
VELOCITY_MODE = 1
MAX_VELOCITY = 460

class DynamixelDriver(Node):
    def __init__(self):
        super().__init__('dynamixel_driver')
        
        self.port = PortHandler(DEVICE)
        self.packet = PacketHandler(2.0)
        
        if not self.port.openPort():
            self.get_logger().error('Failed to open port!')
            return
        self.port.setBaudRate(BAUDRATE)
        
        # Set velocity mode
        self.packet.write1ByteTxRx(self.port, LEFT_ID, MODE_ADDR, VELOCITY_MODE)
        self.packet.write1ByteTxRx(self.port, RIGHT_ID, MODE_ADDR, VELOCITY_MODE)
        
        # Enable torque
        self.packet.write1ByteTxRx(self.port, LEFT_ID, TORQUE_ADDR, 1)
        self.packet.write1ByteTxRx(self.port, RIGHT_ID, TORQUE_ADDR, 1)
        
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        
        self.get_logger().info('Dynamixel driver started!')

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        # Convert to left/right velocities
        left_vel = linear - angular
        right_vel = linear + angular

        # Scale to motor range
        left_raw = int(left_vel * MAX_VELOCITY)
        right_raw = int(right_vel * MAX_VELOCITY)

        # Clamp to valid range
        left_raw = max(-MAX_VELOCITY, min(MAX_VELOCITY, left_raw))
        right_raw = max(-MAX_VELOCITY, min(MAX_VELOCITY, right_raw))

        self.set_velocity(LEFT_ID, left_raw)
        self.set_velocity(RIGHT_ID, right_raw)

        self.get_logger().info(f'Left: {left_raw} Right: {right_raw}')

    def set_velocity(self, motor_id, velocity):
        data = [
            DXL_LOBYTE(DXL_LOWORD(velocity)),
            DXL_HIBYTE(DXL_LOWORD(velocity)),
            DXL_LOBYTE(DXL_HIWORD(velocity)),
            DXL_HIBYTE(DXL_HIWORD(velocity))
        ]
        self.packet.write4ByteTxRx(self.port, motor_id, VELOCITY_ADDR, velocity & 0xFFFFFFFF)

    def destroy_node(self):
        # Stop motors and disable torque on shutdown
        self.set_velocity(LEFT_ID, 0)
        self.set_velocity(RIGHT_ID, 0)
        self.packet.write1ByteTxRx(self.port, LEFT_ID, TORQUE_ADDR, 0)
        self.packet.write1ByteTxRx(self.port, RIGHT_ID, TORQUE_ADDR, 0)
        self.port.closePort()
        super().destroy_node()

def main():
    rclpy.init()
    node = DynamixelDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
