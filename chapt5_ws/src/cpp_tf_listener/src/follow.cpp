#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>
#include <geometry_msgs/msg/transform_stamped.hpp>
#include <geometry_msgs/msg/twist.hpp>
int main(int argc, char *argv[])
{
    // 初始化 ROS2 客户端
    rclcpp::init(argc, argv);
    // 创建节点
    auto node = std::make_shared<rclcpp::Node>("transform_listener");
    auto target = node->declare_parameter<std::string>("target", "new_turtle1");
    auto source = node->declare_parameter<std::string>("source", "turtle1");
    auto twist_pub_ = node->create_publisher<geometry_msgs::msg::Twist>(std::string(target.c_str()) + "/cmd_vel",10);
    // 创建tf2缓冲区
    auto buffer = std::make_shared<tf2_ros::Buffer>(node->get_clock());
    // 创建坐标变换监听器，并绑定tf2缓冲区
    auto tf_listener = std::make_shared<tf2_ros::TransformListener>(*buffer);
    // 设置定时器以持续监听坐标变换
    auto timer = node->create_wall_timer(std::chrono::milliseconds(1000), [&]() {
        // 监听并处理坐标变换
        geometry_msgs::msg::TransformStamped transformStamped;
        try {
            transformStamped = buffer->lookupTransform(target.c_str(), source.c_str(), rclcpp::Time(0));

        } catch (const tf2::TransformException& ex) {
            RCLCPP_ERROR(node->get_logger(), "Transform error: %s", ex.what());
        }
    geometry_msgs::msg::Twist msg;
    static const double scaleRotationRate = 1.0;
    msg.angular.z = scaleRotationRate * atan2(
        transformStamped.transform.translation.y,
        transformStamped.transform.translation.x);

    static const double scaleForwardSpeed = 0.5;
    msg.linear.x = scaleForwardSpeed * sqrt(
        pow(transformStamped.transform.translation.x, 2) +
        pow(transformStamped.transform.translation.y, 2));

    twist_pub_->publish(msg);

    });
    // 进入 ROS2 事件循环
    rclcpp::spin(node);
    // 关闭 ROS2 客户端
    rclcpp::shutdown();
    return 0;
}
