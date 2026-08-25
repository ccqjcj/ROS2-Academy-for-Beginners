from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node'
        ),
        Node(
            package='cpp_tf_listener',
            executable='spawn',
        ),
        Node(
            package='cpp_tf_broadcaster',
            executable='dynamic_new',
            name='broadcaster1',
            parameters=[
                {'turtlename': 'turtle1'},
            ]
        ),
        Node(
            package='cpp_tf_broadcaster',
            executable='dynamic_new',
            name='broadcaster2',
            parameters=[
                {'turtlename': 'turtle2'}
            ]
        ),
        Node(
            package='cpp_tf_listener',
            executable='follow',
            parameters=[
                {'target': 'turtle2'},
                {'source': 'turtle1'}
            ]
        ),
    ])