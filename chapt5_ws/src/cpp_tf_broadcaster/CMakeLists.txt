cmake_minimum_required(VERSION 3.8)
project(cpp_tf_broadcaster)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)

add_executable(dynamic_broadcast src/dynamic_broadcast.cpp)
add_executable(static_broadcast src/static_broadcast.cpp)
add_executable(tf_point_broadcaster src/tf_point_broadcaster.cpp)
add_executable(tf_dynamic_broadcaster src/tf_dynamic_broadcaster.cpp)
add_executable(tf_static_broadcaster src/tf_static_broadcaster.cpp)
target_include_directories(tf_static_broadcaster PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(tf_static_broadcaster PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  tf_static_broadcaster
  "rclcpp"
  "tf2"
  "tf2_ros"
  "geometry_msgs"
  "turtlesim"
)
ament_target_dependencies(
  tf_dynamic_broadcaster
  "rclcpp"
  "tf2"
  "tf2_ros"
  "geometry_msgs"
  "turtlesim"
)
ament_target_dependencies(
  tf_point_broadcaster
  "rclcpp"
  "tf2"
  "tf2_ros"
  "geometry_msgs"
  "turtlesim"
)
ament_target_dependencies(
  static_broadcast
  "rclcpp"
  "tf2"
  "tf2_ros"
  "geometry_msgs"
  "turtlesim"
)
ament_target_dependencies(
  dynamic_broadcast
  "rclcpp"
  "tf2"
  "tf2_ros"
  "geometry_msgs"
  "turtlesim"
)
install(TARGETS 
        tf_static_broadcaster 
        tf_dynamic_broadcaster 
        tf_point_broadcaster
        static_broadcast
        dynamic_broadcast
        DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
