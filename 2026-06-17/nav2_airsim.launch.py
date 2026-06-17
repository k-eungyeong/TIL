[ launch/nav2_airsim.launch.py ]

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('airsim_nav2')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # ── 런치 인자 ──────────────────────────────────
    map_yaml = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    declare_map = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(pkg_dir, 'maps', 'blocks_map.yaml'),
        description='Full path to map yaml file'
    )

    # ── Nav2 Bringup (localization + navigation) ──
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml,
            'use_sim_time': use_sim_time,
            'params_file': os.path.join(pkg_dir, 'config', 'nav2_params.yaml'),
            'autostart': 'true',
        }.items()
    )

    # ── cmd_vel → AirSim 브리지 ───────────────────
    bridge_node = Node(
        package='airsim_nav2',
        executable='cmd_vel_bridge',
        name='cmd_vel_bridge',
        parameters=[{
            'use_sim_time': use_sim_time,
            'wheelbase': 2.5,
            'max_steering_angle': 0.5,
            'max_speed': 5.0,
            'throttle_gain': 0.3,
        }],
        output='screen'
    )

    # ── Static TF: base_link → laser (에어심 전용 좌표계 동기화) ──
    # 변경: 이전 단계에서 성공한 프레임 네이밍 규칙(Humble 신형 옵션)을 명시합니다.
    static_tf_laser = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_base_to_laser',
        arguments=[
            '--x', '0.0', 
            '--y', '0.0', 
            '--z', '0.5', 
            '--yaw', '0.0', 
            '--pitch', '0.0', 
            '--roll', '0.0',
            '--frame-id', 'Car1/Car1',   # 에어심 차량 중심 명칭
            '--child-frame-id', 'Car1/LidarSensor' # 에어심 라이다 프레임 명칭
        ]
    )

    return LaunchDescription([
        declare_map,
        static_tf_laser, # 만약 SLAM 런치와 동시에 켜서 중복 경고가 난다면 이 줄만 주석처리 하세요.
        bridge_node,
        nav2_launch,
    ])
