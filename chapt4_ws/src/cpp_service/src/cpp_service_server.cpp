#include "example_interfaces/srv/add_two_ints.hpp"
#include "rclcpp/rclcpp.hpp"


class ServiceServer : public rclcpp::Node {
public:
  ServiceServer(std::string name) : Node(name) {
    RCLCPP_INFO(this->get_logger(), "%s已启动.", name.c_str());

     add_ints_server_ =
      this->create_service<example_interfaces::srv::AddTwoInts>(
        "add_two_ints_srv",
        std::bind(&ServiceServer::handle_add_two_ints, this,
                  std::placeholders::_1, std::placeholders::_2));
  }

private:

  rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr
    add_ints_server_;

  void handle_add_two_ints(
    const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
    std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response) {
    RCLCPP_INFO(this->get_logger(), "a: %ld b: %ld", request->a,
                request->b);
    response->sum = request->a + request->b;
  };
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ServiceServer>("cpp_service_server");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}