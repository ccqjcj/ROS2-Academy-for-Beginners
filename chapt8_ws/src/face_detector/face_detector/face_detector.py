import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import os
import numpy as np
# from PIL import Image

class ImageConverter(Node):
    def __init__(self):
        super().__init__('cv_bridge_test')
        self.bridge = CvBridge()

        # # 声明图像的发布者和订阅者
        self.image_pub = self.create_publisher(Image, "cv_bridge_image", 10)
        self.image_sub = self.create_subscription(Image, "/image_raw", self.callback, 10)
        self.recognizer=cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('/home/ant/ros/cv_ws/src/face_detector/resource/trainer.yml')

    def callback(self, data):
        # 使用 cv_bridge 将 ROS 的图像数据转换成 OpenCV 的图像格式
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridge.CvBridgeError as e:
            self.get_logger().error(f"CV Bridge Error: {e}")
            return

        # 转换为灰度图像
        self.gray_img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
        self.face_recognition()

            
    def face_detect(self):
        # 加载人脸检测的分类器
        face_detector = cv2.CascadeClassifier(
            r'/home/ant/ros/cv_ws/src/face_detector/resource/haarcascade_frontalface_alt.xml'
        )
        
        # 检测人脸
        faces = face_detector.detectMultiScale(self.gray_img, 1.3, 5)
        
        # 在检测到的人脸上绘制矩形框
        for (x, y, w, h) in faces:
            cv2.rectangle(self.cv_image, (x, y), (x + w, y + h), (0, 0, 255), 6)

        # 显示图像窗口
        cv2.imshow("Image window", self.cv_image)
        cv2.waitKey(3)

        # 将 OpenCV 格式的数据转换成 ROS 图像格式发布
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.cv_image, "bgr8"))
        except CvBridge.CvBridgeError as e:
            self.get_logger().error(f"CV Bridge Error: {e}")


    def face_recognition(self):
        # 加载人脸检测的分类器
        face_detector = cv2.CascadeClassifier(
            r'/home/ant/ros/cv_ws/src/face_detector/resource/haarcascade_frontalface_alt.xml'
        )
        
        # 检测人脸
        faces = face_detector.detectMultiScale(self.gray_img, 1.3, 5)
        
        # 在检测到的人脸上绘制矩形框
        for (x, y, w, h) in faces:
            cv2.rectangle(self.cv_image, (x, y), (x + w, y + h), (0, 0, 255), 6)
            id,_ = self.recognizer.predict(self.gray_img[y:y+h,x:x+w])
            text = "yfl" if id == 1 else ""  # 如果 id == 1, 显示 'yfl'，否则显示空字符串
            cv2.putText(self.cv_image, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (128, 128, 0), 2)
        # 显示图像窗口
        cv2.imshow("Image window", self.cv_image)
        cv2.waitKey(3)

        # 将 OpenCV 格式的数据转换成 ROS 图像格式发布
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.cv_image, "bgr8"))
        except CvBridge.CvBridgeError as e:
            self.get_logger().error(f"CV Bridge Error: {e}")


def getImageAndLabels(path):
    facesSample = []  # 用于存储人脸区域的列表
    ids = []  # 用于存储每张人脸对应的ID
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # 获取路径中所有图像文件的完整路径

    # 使用预训练的人脸分类器进行人脸检测，CascadeClassifier是一种级联分类器
    face_detector = cv2.CascadeClassifier(
        r'/home/ant/ros/cv_ws/src/face_detector/resource/haarcascade_frontalface_alt.xml'
    )
    for imagePath in imagePaths:
        try:
            # 打开图像并将其转换为灰度图，因为人脸检测通常在灰度图像上效果更好
            PIL_image = Image.open(imagePath).convert('L')
        except Exception as e:
            print(f"Error opening image {imagePath}: {e}")  # 如果图像打开失败，打印错误信息
            continue

        img_numpy = np.array(PIL_image, 'uint8')  # 将图像转换为NumPy数组，用于后续处理
        # 使用分类器检测图像中的人脸，返回的是人脸区域的坐标列表
        faces = face_detector.detectMultiScale(img_numpy, scaleFactor=1.2, minNeighbors=5)

        # 从文件名中提取ID，假设文件名的格式为 "ID.其他扩展名"
        id = int(os.path.split(imagePath)[1].split('.')[0])

        # 遍历检测到的人脸区域
        for (x, y, w, h) in faces:
            # 确保人脸的坐标在图像边界内
            if x + w <= img_numpy.shape[1] and y + h <= img_numpy.shape[0]:
                # 截取人脸区域，并添加到人脸样本列表中
                facesSample.append(img_numpy[y:y + h, x:x + w])
                # 添加对应的ID到列表
                ids.append(id)
    return facesSample, ids

def main(args=None):
    #  # 设置人脸图像所在的文件夹路径
    # path = '/home/ant/ros/cv_ws/src/face_detector/resource/image'
 
    # # 调用函数获取图像中的人脸和对应的ID
    # faces, ids = getImageAndLabels(path)
 
    # # OpenCV的新版本不再支持face模块，但这里是使用旧版的face识别器
    # recognizer = cv2.face.LBPHFaceRecognizer_create()  # 创建LBPH人脸识别器
    # recognizer.train(faces, np.array(ids))  # 使用获取到的人脸和ID列表训练识别器
 
    # # 将训练好的模型保存到指定文件
    # recognizer.write('/home/ant/ros/cv_ws/src/face_detector/resource/trainer.yml')

    rclpy.init(args=args)
    node = ImageConverter()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down cv_bridge_test node.")
    finally:
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
