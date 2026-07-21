#!/usr/bin/env python3

import rclpy

from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args)

    node1 = Node("my_node")
    node1.get_logger().info('Hi from my_node.')

    rclpy.spin(node1)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
