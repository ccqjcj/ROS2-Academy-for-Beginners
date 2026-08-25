#include "turtlesim/srv/spawn.hpp"
#include "rclcpp/rclcpp.hpp"

int main(int argc, char * argv[])
{
    // 初始化 ROS 2 节点
    rclcpp::init(argc, argv);

    // 创建节点
    auto node = std::make_shared<rclcpp::Node>("turtle_spawner");

    // 创建乌龟生成服务的客户端
    auto client = node->create_client<turtlesim::srv::Spawn>("spawn");
    auto turtle_name = node->declare_parameter<std::string>("turtle_name", "turtle2");

    // 等待乌龟生成服务就绪
    if (!client->wait_for_service(std::chrono::seconds(1))) {
        RCLCPP_ERROR(node->get_logger(), "Failed to wait for the service. Exiting.");
        return -1;
    }

    // 创建请求
    auto request = std::make_shared<turtlesim::srv::Spawn::Request>();
    request->x = 4.0; // 乌龟的初始 x 坐标
    request->y = 2.0; // 乌龟的初始 y 坐标
    request->theta = 0.0; // 乌龟的初始角度
    request->name = turtle_name.c_str(); // 乌龟的名称

    // 发送请求
    auto result = client->async_send_request(request);

    // 等待响应
    if (rclcpp::spin_until_future_complete(node, result) !=
        rclcpp::FutureReturnCode::SUCCESS)
    {
        RCLCPP_ERROR(node->get_logger(), "Failed to spawn turtle.");
        return -1;
    }

    RCLCPP_INFO(node->get_logger(), "Turtle spawned successfully.");

    // 关闭节点
    rclcpp::shutdown();

    return 0;
}
