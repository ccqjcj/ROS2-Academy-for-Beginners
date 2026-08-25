#include <geometry_msgs/msg/transform_stamped.hpp>
#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/transform_broadcaster.h>
#include <turtlesim/msg/pose.hpp>

int main(int argc, char * argv[])
{
    // 初始化 ROS 客户端
    rclcpp::init(argc, argv);
    
    // 创建节点
    auto node = std::make_shared<rclcpp::Node>("minimal_dynamic_frame_broadcaster");
    // 创建坐标变换广播器
    auto tf_broadcaster = std::make_shared<tf2_ros::TransformBroadcaster>(node);

    auto turtlename_ = node->declare_parameter<std::string>("turtlename", "turtle1");
    std::string topic_name = std::string(turtlename_.c_str()) + "/pose";
    // 创建乌龟位姿订阅器
    auto subscription = node->create_subscription<turtlesim::msg::Pose>(
        topic_name, 10,
        [&](const turtlesim::msg::Pose::SharedPtr msg) {
            // 组织消息
            geometry_msgs::msg::TransformStamped t;
            t.header.stamp = node->now();
            t.header.frame_id = "world";
            t.child_frame_id = turtlename_.c_str();
            t.transform.translation.x = msg->x;
            t.transform.translation.y = msg->y;
            t.transform.translation.z = 0.0;
            tf2::Quaternion q;
            q.setRPY(0, 0, msg->theta);
            t.transform.rotation.x = q.x();
            t.transform.rotation.y = q.y();
            t.transform.rotation.z = q.z();
            t.transform.rotation.w = q.w();
            // 发布消息
            tf_broadcaster->sendTransform(t);
        });

    // 进入 ROS 事件循环
    rclcpp::spin(node);
    // 关闭 ROS 客户端
    rclcpp::shutdown();
    return 0;
}
