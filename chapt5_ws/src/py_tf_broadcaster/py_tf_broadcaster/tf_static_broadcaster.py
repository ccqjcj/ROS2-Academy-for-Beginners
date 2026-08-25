import sys
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
import tf_transformations

class MinimalStaticFrameBroadcasterPy(Node):

    def __init__(self, transformation):
        super().__init__('minimal_static_frame_broadcaster_py')
        self._tf_publisher = StaticTransformBroadcaster(self)
        self.make_transforms(transformation)

    def make_transforms(self, transformation):
        static_transformStamped = TransformStamped()
        static_transformStamped.header.stamp = self.get_clock().now().to_msg()
        static_transformStamped.header.frame_id = sys.argv[7]
        static_transformStamped.child_frame_id = sys.argv[8]
        static_transformStamped.transform.translation.x = float(sys.argv[1])
        static_transformStamped.transform.translation.y = float(sys.argv[2])
        static_transformStamped.transform.translation.z = float(sys.argv[3])
        quat = tf_transformations.quaternion_from_euler(
            float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))
        static_transformStamped.transform.rotation.x = quat[0]
        static_transformStamped.transform.rotation.y = quat[1]
        static_transformStamped.transform.rotation.z = quat[2]
        static_transformStamped.transform.rotation.w = quat[3]
        self._tf_publisher.sendTransform(static_transformStamped)


def main():
    logger = rclpy.logging.get_logger('logger')
    if len(sys.argv) < 9:
        logger.info('运行程序时请按照：x y z roll pitch yaw frame_id child_frame_id 的格式传入参数')
        sys.exit(0)

    rclpy.init()
    node = MinimalStaticFrameBroadcasterPy(sys.argv)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()