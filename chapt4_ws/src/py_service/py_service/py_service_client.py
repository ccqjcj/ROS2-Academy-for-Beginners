#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceClient(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("%s已启动." % name)
        self.client_ = self.create_client(AddTwoInts,"add_two_ints_srv") 

    def result_callback_(self, result_future):
        response = result_future.result()
        self.get_logger().info(f"结果：{response.sum}")
    
    def send_request(self, a, b):
        while rclpy.ok() and self.client_.wait_for_service(1)==False:
            self.get_logger().info(f"等待...")
            
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        self.client_.call_async(request).add_done_callback(self.result_callback_)

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = ServiceClient("py_service_client")  # 新建一个节点
    node.send_request(1,2)
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy