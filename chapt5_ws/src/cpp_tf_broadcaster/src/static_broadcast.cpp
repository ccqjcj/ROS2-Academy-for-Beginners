#include <geometry_msgs/msg/transform_stamped.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/static_transform_broadcaster.h>
#include <rclcpp/rclcpp.hpp>

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    if (argc != 9)
    {
        std::cerr << "x y z pitch yaw roll frame_id child_frame_id" << std::endl;
        return 1;
    }
    auto node = std::make_shared<rclcpp::Node>("static_tf_publisher");
    auto tf_publisher = std::make_shared<tf2_ros::StaticTransformBroadcaster>(node);

    geometry_msgs::msg::TransformStamped transformStamped;
    transformStamped.header.stamp = rclcpp::Clock().now();
    transformStamped.header.frame_id = argv[7];
    transformStamped.child_frame_id = argv[8];

    transformStamped.transform.translation.x = atof(argv[1]);
    transformStamped.transform.translation.y = atof(argv[2]);
    transformStamped.transform.translation.z = atof(argv[3]);

    tf2::Quaternion q;
    q.setRPY(atof(argv[4]), atof(argv[5]), atof(argv[6]));
    transformStamped.transform.rotation.x = q.x();
    transformStamped.transform.rotation.y = q.y();
    transformStamped.transform.rotation.z = q.z();
    transformStamped.transform.rotation.w = q.w();

    tf_publisher->sendTransform(transformStamped);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
