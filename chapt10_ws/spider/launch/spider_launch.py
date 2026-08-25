from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
import os

sdfdir='/home/hw1/my_ws/src/spider/sdf/'
SDF_WORLD_PATH=sdfdir+'spider.world'
SDF_MODEL_PATH=sdfdir+'spider.sdf'

def loadsdfmodel(sdfmodelpath):
    with open(sdfmodelpath) as f:
        dirname=os.path.dirname(sdfmodelpath)
        print(dirname)
        robot_desc = f.read()
        robot_desc = robot_desc.replace('model://','file://'+sdfdir)
        return robot_desc
    print('sdf model is not exists')

def generate_launch_description():
    #launch a gazebo world for simulation
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch/gz_sim.launch.py')),launch_arguments=[('gz_args',SDF_WORLD_PATH)]
    )
    
    #add model to gazebo
    sdfmodelstr=loadsdfmodel(SDF_MODEL_PATH)
    addrobottogazebo=Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-world', 'spider', '-name',f'spider','-string',
                   sdfmodelstr,'-x','0','-y','0','-z','0.25'])

    #bridge gazebo msg to ros
    bridgenode=Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[ {'config_file':sdfdir+'jointcontroltopicmap.yaml'},]
        )

    #publish model to ros by robot state publisher, which make robot can be seen in rviz2
    robotinros=Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': sdfmodelstr},
        ]
        )

    # start rviz2 node
    rviz=Node(
            package='rviz2',
            executable='rviz2',
            parameters=[ {'config_file':sdfdir+'spider.rviz'},{'use_sim_time': True}],           
        )
    
    #robot control node 
    learnstep=Node(package='spider',
        executable='learnstep')
    return LaunchDescription([
        gazebo_launch,
        addrobottogazebo,
        bridgenode,
        robotinros,
        rviz,
    #    learnstep
    ])