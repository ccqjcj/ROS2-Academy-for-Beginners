#include <cstdio>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <rclcpp/rclcpp.hpp>

using namespace cv;
void callback(const sensor_msgs::msg::Image::ConstSharedPtr& msg)
{
  cv::Mat image = cv_bridge::toCvShare(msg,"bgr8")->image;
  cv::imshow("Camera", image); 
  cv::waitKey(1);
}
int main(int argc,char **argv)
{
  rclcpp::init(argc,argv);
  auto node = rclcpp::Node::make_shared("pub");
  image_transport::ImageTransport it(node);
  image_transport::Subscriber sub = it.subscribe("camera/image",1,callback);
  cv::namedWindow("Image",cv::WINDOW_AUTOSIZE);

  rclcpp::spin(node);
  cv::destroyAllWindows();
  rclcpp::shutdown();
  return 0;
}
