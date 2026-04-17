import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from std_srvs.srv import Trigger
from dynamixel_sdk import *

DEVICE = '/dev/ttyUSB0'
BAUDRATE = 57600

RIGHT_IDS = [1, 3, 5]
LEFT_IDS = [2, 4, 6]

MODE_ADDR = 11
TORQUE_ADDR = 64
VELOCITY_ADDR = 104
PRESENT_POSITION_ADDR = 132
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
        
        # Set velocity mode and enable torque for all motors
        for motor_id in RIGHT_IDS + LEFT_IDS:
            self.packet.write1ByteTxRx(self.port, motor_id, MODE_ADDR, VELOCITY_MODE)
            self.packet.write1ByteTxRx(self.port, motor_id, TORQUE_ADDR, 1)
            self.get_logger().info(f'Motor {motor_id} ready')

        # Subscriber for cmd_vel
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        # Publisher for joint states
        self.state_pub = self.create_publisher(JointState, '/dynamixel_state', 10)
        self.create_timer(0.1, self.publish_state)

        # Service for wheel_command
        self.wheel_srv = self.create_service(
            Trigger, '/wheel_command', self.wheel_command_callback)

        self.left_vel = 0
        self.right_vel = 0
        
        self.get_logger().info('Dynamixel driver started!')

    def publish_state(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['right_1', 'right_3', 'right_5', 'left_2', 'left_4', 'left_6']

        velocities = []
        positions = []
        for motor_id in RIGHT_IDS + LEFT_IDS:
            vel, _, _ = self.packet.read4ByteTxRx(self.port, motor_id, VELOCITY_ADDR)
            pos, _, _ = self.packet.read4ByteTxRx(self.port, motor_id, PRESENT_POSITION_ADDR)
            velocities.append(float(vel))
            positions.append(float(pos))

        msg.velocity = velocities
        msg.position = positions
        self.state_pub.publish(msg)

    def wheel_command_callback(self, request, response):
        self.set_velocity_all(self.right_vel, self.left_vel)
        response.success = True
        response.message = f'Right: {self.right_vel} Left: {self.left_vel}'
        return response

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        left_vel = linear - angular
        right_vel = linear + angular

        # Scale to motor range
        self.left_vel = max(-MAX_VELOCITY, min(MAX_VELOCITY, int(left_vel * MAX_VELOCITY)))
        self.right_vel = max(-MAX_VELOCITY, min(MAX_VELOCITY, int(right_vel * MAX_VELOCITY)))

        self.set_velocity_all(self.right_vel, self.left_vel)
        self.get_logger().info(f'Right: {self.right_vel} Left: {self.left_vel}')

    def set_velocity_all(self, right_vel, left_vel):
        # Right side is reversed so negate it
        for motor_id in RIGHT_IDS:
            self.packet.write4ByteTxRx(self.port, motor_id, VELOCITY_ADDR, (-right_vel) & 0xFFFFFFFF)
        for motor_id in LEFT_IDS:
            self.packet.write4ByteTxRx(self.port, motor_id, VELOCITY_ADDR, left_vel & 0xFFFFFFFF)

    def destroy_node(self):
        # Stop all motors and disable torque on shutdown
        for motor_id in RIGHT_IDS + LEFT_IDS:
            self.packet.write4ByteTxRx(self.port, motor_id, VELOCITY_ADDR, 0)
            self.packet.write1ByteTxRx(self.port, motor_id, TORQUE_ADDR, 0)
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
