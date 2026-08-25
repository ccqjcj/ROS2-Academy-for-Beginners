from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
import tf_transformations
from turtlesim.msg import Pose

# 3.定义节点类；
class MinimalDynamicFrameBroadcasterPy(Node):

    def __init__(self):
        super().__init__('minimal_dynamic_frame_broadcaster_py')

        # 3-1.创建动态坐标变换发布方；
        self.br = TransformBroadcaster(self)
        # 3-2.创建乌龟位姿订阅方；
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.handle_turtle_pose,
            1)
        self.subscription
    # 3-3.根据订阅到的乌龟位姿生成坐标帧并广播。
    def handle_turtle_pose(self, msg):
        # 组织消息
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'turtle1'

        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        q = tf_transformations.quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # 发布消息
        self.br.sendTransform(t)


def main():
    # 2.初始化 ROS 客户端；
    rclpy.init()
    # 4.调用 spin 函数，并传入对象；
    node = MinimalDynamicFrameBroadcasterPy()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    # 5.释放资源。
    rclpy.shutdown()