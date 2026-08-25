from geometry_msgs.msg import PointStamped
import rclpy
from rclpy.node import Node

# 3.定义节点类；
class MinimalPointPublisher(Node):

    def __init__(self):
        super().__init__('minimal_point_publisher_py')
        # 3-1.创建坐标点发布方；
        self.pub = self.create_publisher(PointStamped, 'point', 10)
        # 3-2.创建定时器；
        self.timer = self.create_timer(1.0, self.on_timer)
        self.x = 0.1
    def on_timer(self):
        # 3-3.组织并发布坐标点消息。
        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.header.frame_id = 'laser'
        self.x += 0.02
        ps.point.x = self.x
        ps.point.y = 0.0
        ps.point.z = 0.2
        self.pub.publish(ps)


def main():
    # 2.初始化 ROS 客户端；
    rclpy.init()
    # 4.调用 spin 函数，并传入对象；
    node = MinimalPointPublisher()
    rclpy.spin(node)
    # 5.释放资源。3-3.组织并发布坐标点消息。