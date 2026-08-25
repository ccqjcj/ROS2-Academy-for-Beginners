import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class ImageConverter(Node):
    def __init__(self):
        super().__init__('cv_bridge_test')
        self.bridge = CvBridge()

        # 声明图像的发布者和订阅者
        self.image_pub = self.create_publisher(Image, "cv_bridge_image", 10)
        self.image_sub = self.create_subscription(Image, "/image_raw", self.callback, 10)

    def callback(self, data):
        # 使用 cv_bridge 将 ROS 的图像数据转换成 OpenCV 的图像格式
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridge.CvBridgeError as e:
            self.get_logger().error(f"CV Bridge Error: {e}")
            return

        # 在 OpenCV 的显示窗口中绘制一个圆作为标记
        (rows, cols, channels) = cv_image.shape
        if cols > 60 and rows > 60:
            cv2.circle(cv_image, (60, 60), 30, (0, 0, 255), -1)

        # 显示 OpenCV 格式的图像
        cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)

        # 再将 OpenCV 格式的数据转换成 ROS image 格式的数据发布
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridge.CvBridgeError as e:
            self.get_logger().error(f"CV Bridge Error: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = ImageConverter()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down cv_bridge_test node.")
    finally:
        cv2.destroyAllWindows()
        rclpy.shutdown()
