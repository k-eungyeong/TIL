[ airsim_nav2/airsim_nav2/cmd_vel_bridge.py ]

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from airsim_interfaces.msg import CarControls
import math


class CmdVelBridge(Node):
    def __init__(self):
        super().__init__('cmd_vel_bridge')

        self.declare_parameter('wheelbase', 2.5)
        self.declare_parameter('max_steering_angle', 0.5)
        self.declare_parameter('max_speed', 5.0)
        self.declare_parameter('throttle_gain', 0.3)

        self.wheelbase     = self.get_parameter('wheelbase').value
        self.max_steer     = self.get_parameter('max_steering_angle').value
        self.max_speed     = self.get_parameter('max_speed').value
        self.throttle_gain = self.get_parameter('throttle_gain').value

        self.last_linear_x = 0.0

        self.sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.pub = self.create_publisher(
            CarControls, '/airsim_node/Car1/car_cmd', 10)

        self.get_logger().info('CmdVelBridge started.')

    def cmd_vel_callback(self, msg: Twist):
        controls = CarControls()
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # ── 조향 계산 ────────────────────────────────────────────────
        ref_speed = linear_x if abs(linear_x) > 0.01 else self.last_linear_x

        if abs(angular_z) > 0.01 and abs(ref_speed) > 0.01:
            steer_rad = math.atan2(self.wheelbase * angular_z, abs(ref_speed))
            steer_rad = max(-self.max_steer, min(self.max_steer, steer_rad))
            controls.steering = -(steer_rad / self.max_steer)
        elif abs(angular_z) > 0.01:
            controls.steering = -math.copysign(0.4, angular_z)
        else:
            controls.steering = 0.0

        # ── 스로틀 / 브레이크 / 기어 계산 ───────────────────────────
        if abs(linear_x) > 0.01:
            throttle_raw = min(
                (abs(linear_x) / self.max_speed) * self.throttle_gain * 3.0,
                1.0
            )
            if linear_x > 0:
                controls.throttle = throttle_raw
                controls.brake = 0.0
                controls.manual = False
                controls.manual_gear = 0
                controls.gear_immediate = True
            else:
                controls.throttle = throttle_raw
                controls.brake = 0.0
                controls.manual = True
                controls.manual_gear = -1
                controls.gear_immediate = True
            controls.handbrake = False
            self.last_linear_x = linear_x

        elif abs(angular_z) > 0.01:
            controls.throttle = 0.0
            controls.brake = 0.0
            controls.manual = False
            controls.manual_gear = 0
            controls.handbrake = False
            controls.gear_immediate = True

        else:
            controls.throttle = 0.0
            controls.brake = 1.0
            controls.steering = 0.0
            controls.manual = False
            controls.manual_gear = 0
            controls.handbrake = False
            controls.gear_immediate = True
            self.last_linear_x = 0.0

        self.pub.publish(controls)

        self.get_logger().debug(
            f'v={linear_x:.2f} w={angular_z:.2f} -> '
            f'thr={controls.throttle:.2f} brk={controls.brake:.2f} '
            f'steer={controls.steering:.2f} gear={controls.manual_gear}')


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
