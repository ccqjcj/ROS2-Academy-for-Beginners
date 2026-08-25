from launch import LaunchDescription
from launch_ros.actions import Node # type: ignore

def generate_launch_description():

    t1 = Node(package="turtlesim", namespace="turtlesim1", executable="turtlesim_node", name="t1")
    t2 = Node(package="turtlesim", namespace="turtlesim2", executable="turtlesim_node", name="t2")
    mimic = Node(
                 package="turtlesim", 
                 executable="mimic", 
                 name="mimic",
                 remappings=[                 
                    ('/input/pose', '/turtlesim1/turtle1/pose'),        
                    ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),  
                ]
                )
    
    return LaunchDescription([t1, t2, mimic])


