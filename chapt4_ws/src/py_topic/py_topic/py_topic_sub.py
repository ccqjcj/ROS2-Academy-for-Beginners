#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class NodeSubscribe02(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("%s已启动" % name)
        self.command_subscribe_ = self.create_subscription(String,"command",self.command_callback,10)

    def command_callback(self,msg):
          if msg.data=="hello world":
           self.get_logger().info(f'收到[{msg.data}]命令')

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = NodeSubscribe02("py_topic_sub")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy