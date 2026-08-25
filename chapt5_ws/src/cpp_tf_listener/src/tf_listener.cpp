#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>
#include <geometry_msgs/msg/transform_stamped.hpp>

int main(int argc, char *argv[])
{
    // 初始化 ROS2 客户端
    rclcpp::init(argc, argv);
    // 创建节点
    auto node = std::make_shared<rclcpp::Node>("transform_listener");
    auto target = node->declare_parameter<std::string>("target", "turtle1");
    auto source = node->declare_parameter<std::string>("source", "world");
    // 创建tf2缓冲区
    auto buffer = std::make_shared<tf2_ros::Buffer>(node->get_clock());
    // 创建坐标变换监听器，并绑定tf2缓冲区
    auto tf_listener = std::make_shared<tf2_ros::TransformListener>(*buffer);
    // 设置定时器以持续监听坐标变换
    auto timer = node->create_wall_timer(std::chrono::milliseconds(1000), [&]() {
        // 监听并处理坐标变换
        geometry_msgs::msg::TransformStamped transform_stamped;
        try {
            transform_stamped = buffer->lookupTransform(target.c_str(), source.c_str(), rclcpp::Time(0));
            // 打印接收到的坐标变换信息
            RCLCPP_INFO(node->get_logger(),
                         "Translation: (%f, %f, %f), Rotation: (%f, %f, %f, %f)",
                         transform_stamped.transform.translation.x,
                         transform_stamped.transform.translation.y,
                         transform_stamped.transform.translation.z,
                         transform_stamped.transform.rotation.x,
                         transform_stamped.transform.rotation.y,
                         transform_stamped.transform.rotation.z,
                         transform_stamped.transform.rotation.w);
        } catch (const tf2::TransformException& ex) {
            RCLCPP_ERROR(node->get_logger(), "Transform error: %s", ex.what());
        }
    });
    // 进入 ROS2 事件循环
    rclcpp::spin(node);
    // 关闭 ROS2 客户端
    rclcpp::shutdown();
    return 0;
}
