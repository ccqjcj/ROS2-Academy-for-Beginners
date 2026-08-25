#include <cstdio>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <rclcpp/rclcpp.hpp>

using namespace cv;


int main(int argc,char **argv)
{
  rclcpp::init(argc,argv);
  auto node = rclcpp::Node::make_shared("pub");
  image_transport::ImageTransport it(node);
  image_transport::Publisher image_pub = it.advertise("camera/image",1);

  VideoCapture cap(0); 
  sensor_msgs::msg::Image::SharedPtr msg;

  if (!cap.isOpened()) {
    std::cout<<"无法的开摄像头"<<std::endl;
  }
  // 创建一个定时器，用于定时发布消息
  auto timer = node->create_wall_timer(std::chrono::seconds(1), [&]() {
    cv::Mat frame;
    cap.read(frame);   
    msg = cv_bridge::CvImage(std_msgs::msg::Header(),"bgr8",frame).toImageMsg();
    image_pub.publish(msg);
    RCLCPP_INFO(node->get_logger(), "**********************/n");
  });
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}