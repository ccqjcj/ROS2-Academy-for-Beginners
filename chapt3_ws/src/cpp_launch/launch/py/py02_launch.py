from launch import LaunchDescription                   
from launch.actions import DeclareLaunchArgument       # type: ignore #
from launch.substitutions import LaunchConfiguration, TextSubstitution # type: ignore
from launch_ros.actions import Node                    # type: ignore 

def generate_launch_description():                    
   background_r_launch_arg = DeclareLaunchArgument(
      'background_r', default_value=TextSubstitution(text='0')     
   )
   background_g_launch_arg = DeclareLaunchArgument(
      'background_g', default_value=TextSubstitution(text='255')    
   )
   background_b_launch_arg = DeclareLaunchArgument(
      'background_b', default_value=TextSubstitution(text='0')   
   )

   return LaunchDescription([                                      
      background_r_launch_arg,                                     
      background_g_launch_arg,
      background_b_launch_arg,
      Node(                                                       
         package='turtlesim',
         executable='turtlesim_node',                              
         name='sim',                                              
         parameters=[{                                             
            'background_r': LaunchConfiguration('background_r'),   
            'background_g': LaunchConfiguration('background_g'),   
            'background_b': LaunchConfiguration('background_b'),  
         }]
      ),
   ])