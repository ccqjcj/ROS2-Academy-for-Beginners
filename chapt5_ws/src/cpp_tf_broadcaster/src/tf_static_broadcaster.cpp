#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/static_transform_broadcaster.h>
#include <geometry_msgs/msg/transform_stamped.hpp>

using std::placeholders::_1;

class MinimalStaticFrameBroadcaster : public rclcpp::Node
{
public:
  MinimalStaticFrameBroadcaster(char * transformation[]): Node("minimal_static_frame_broadcaster")
  {
    tf_publisher_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    this->make_transforms(transformation);
  }

private:
  void make_transforms(char * transformation[])
  {
    geometry_msgs::msg::TransformStamped t;

    rclcpp::Time now = this->get_clock()->now();
    t.header.stamp = now;
    t.header.frame_id = transformation[7];
    t.child_frame_id = transformation[8];

    t.transform.translation.x = atof(transformation[1]);
    t.transform.translation.y = atof(transformation[2]);
    t.transform.translation.z = atof(transformation[3]);
    tf2::Quaternion q;
    q.setRPY(
      atof(transformation[4]),
      atof(transformation[5]),
      atof(transformation[6]));
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

    tf_publisher_->sendTransform(t);
  }
  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_publisher_;
};

int main(int argc, char * argv[])
{
  auto logger = rclcpp::get_logger("logger");

  if (argc != 9) {
    RCLCPP_INFO(
      logger, "运行程序时请按照：x y z roll pitch yaw frame_id child_frame_id 的格式传入参数");
    return 1;
  }

  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalStaticFrameBroadcaster>(argv));
  rclcpp::shutdown();
  return 0;
}