[ launch/airsim_slam.launch.py ]

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')

    pointcloud_to_laserscan = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        remappings=[
            ('cloud_in', '/airsim_node/Car1/gpulidar/points/LidarSensor'),
            ('scan',     '/scan'),                         # scan 이라는 통신 채널(topic)이 하나 발행됨 -> topic list에 보여야 함
        ],
        parameters=[{
            'target_frame':        'Car1/Car1',
            'transform_tolerance':  0.5,
            'min_height':           0.10,
            'max_height':           1.50,
            'angle_min':           -3.14159,
            'angle_max':            3.14159,
            'angle_increment':      0.00873,
            'scan_time':            0.1,
            'range_min':            1.0,
            'range_max':           30.0,
            'use_inf':              True,
            'queue_size':           50,
            'use_sim_time':         True,
        }],
        output='screen'
    )

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_dir, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'slam_params_file': os.path.join(
                get_package_share_directory('airsim_slam_bringup'),
                'config', 'slam_toolbox_params.yaml'                    # 여기서 slam ~ 은 설정 파일. 
                                                                        # 그래서 config 아래 slam~ 파일이 있는 것이 규칙
            ),
            'use_sim_time': 'true',
        }.items()
    )

    return LaunchDescription([
        TimerAction(period=5.0, actions=[pointcloud_to_laserscan]),
        TimerAction(period=8.0, actions=[slam_toolbox]),
    ])
