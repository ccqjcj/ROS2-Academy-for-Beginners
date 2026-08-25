#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class TopicSubscribe : public rclcpp::Node
{
public:
    TopicSubscribe(std::string name) : Node(name)
    {
        RCLCPP_INFO(this->get_logger(), "%s已启动.", name.c_str());
        command_subscribe_ = this->create_subscription<std_msgs::msg::String>("command", 10, std::bind(&TopicSubscribe::command_callback, this, std::placeholders::_1));
    }

private:
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr command_subscribe_;
    void command_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        if(msg->data == "hello world")
        RCLCPP_INFO(this->get_logger(), "收到[%s]指令", msg->data.c_str());
    }
};


int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TopicSubscribe>("topic_subscribe");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}