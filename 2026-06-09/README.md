# 2026-06-09
### 배운 내용
##### [ 1교시 ]  
<img width="1000" height="840" alt="image" src="https://github.com/user-attachments/assets/fb1ff28e-6d27-42da-a620-1813da03fddf" />

##### [ 2교시 ]  
<img width="998" height="373" alt="image" src="https://github.com/user-attachments/assets/40edbad5-07d2-4ce8-ae8d-29a929fefb35" />
<img width="1000" height="491" alt="image" src="https://github.com/user-attachments/assets/abb7866a-f15d-4d70-aa2c-db56b179f4bc" />

##### [ 3교시 ]  
<img width="993" height="423" alt="image" src="https://github.com/user-attachments/assets/3dbdb008-e6a8-46b5-b14b-ce5a7305b80f" />
```
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    slam_toolbox_dir = get_package_share_directory('slam_toolbox')

    # ── 1. Static TF: 로봇 몸체(Car1/odom_local) → 라이다 센서(Car1/LidarSensor) ──
    # 에어심이 제공하는 두 좌표계의 이름을 부모와 자식으로 정확히 연결합니다.
    static_tf_lidar = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_base_to_lidar',
        arguments=[
            '--x', '0.0',
            '--y', '0.0',
            '--z', '0.5',  # AirSim의 -0.5를 ROS2의 상단 방향인 +0.5로 보정
            '--yaw', '0.0',
            '--pitch', '0.0',
            '--roll', '0.0',
            '--frame-id', 'Car1/odom_local',   # 부모 프레임 명시
            '--child-frame-id', 'Car1/LidarSensor' # 자식 프레임 명시
        ],
        output='screen'
    )

    # ── 2. PointCloud2 → LaserScan 변환 ───────────────────────────────
    pointcloud_to_laserscan = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        remappings=[
            ('cloud_in', '/airsim_node/Car1/lidar/points/LidarSensor'),
            ('scan',     '/scan'),
        ],
        parameters=[{
            'target_frame':   'Car1/LidarSensor',
            'transform_tolerance': 1.0,      # 변경: 시간 동기화 오차 허용 범위를 1초로 크게 확장
            'min_height':     -0.5,
            'max_height':      0.5,
            'angle_min':      -3.14159,
            'angle_max':       3.14159,
            'angle_increment': 0.00873,
            'scan_time':       0.1,
            'range_min':       0.3,
            'range_max':       50.0,
            'use_inf':         True,
            'queue_size':      50,
            'use_sim_time':    True,     # 변경/추가: 시뮬레이션 시간 활성화
        }],
        output='screen'
    )

    # ── 3. SLAM Toolbox (online async 모드) ───────────────────────────
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_dir, 'launch',
                         'online_async_launch.py')
        ),
        launch_arguments={
            'slam_params_file': os.path.join(
                get_package_share_directory('airsim_slam_bringup'),
                'config', 'slam_toolbox_params.yaml'
            ),
            'use_sim_time': 'true',    # 변경: false에서 true로 수정하여 AirSim 시간 추적
        }.items()
    )

    return LaunchDescription([
        static_tf_lidar,
        pointcloud_to_laserscan,
        slam_toolbox,
    ])
```
- “config/slam_toolbox_params.yaml”        # config 아래쪽에 빈 파일 하나 만들기
```

slam_toolbox:
  ros__parameters:

    # ── 기본 설정 ──────────────────────────────────────────────────────
    use_sim_time:  true # 변경: false에서 true로 수정
    solver_plugin: solver_plugins::CeresSolver
    ceres_linear_solver: SPARSE_NORMAL_CHOLESKY
    ceres_preconditioner: SCHUR_JACOBI
    ceres_trust_strategy: LEVENBERG_MARQUARDT
    ceres_dogleg_type: TRADITIONAL_DOGLEG
    ceres_loss_function: None

    # ── 좌표계 ─────────────────────────────────────────────────────────
    # 변경: 에어심 odom 토픽의 frame_id인 'Car1'을 입력합니다. (지도의 기준 원점)
    odom_frame:       Car1

    map_frame:        map

    # 변경: 에어심 odom 토픽의 child_frame_id인 'Car1/odom_local'을 입력합니다. (로봇 중심)
    base_frame:       Car1/odom_local

    scan_topic:       /scan       # pointcloud_to_laserscan 출력

    # ── 동작 모드 ──────────────────────────────────────────────────────
    mode: mapping                 # mapping / localization

    # ── 성능 설정 ──────────────────────────────────────────────────────
    debug_logging: false
    throttle_scans: 1
    transform_publish_period: 0.02   # 50Hz TF 퍼블리시
    map_update_interval: 5.0         # 지도 갱신 주기 (초)
    resolution: 0.05                 # 지도 해상도 5cm
    max_laser_range: 50.0
    minimum_time_interval: 0.5
    minimum_range: 0.3
    transform_timeout: 1.0
    tf_buffer_duration: 30.0
    stack_size_to_use: 40000000      # 40MB

    # ── 루프 클로저 ────────────────────────────────────────────────────
    enable_interactive_mode: true
    use_scan_matching: true
    use_scan_barycenter: true
    minimum_travel_distance: 0.5     # 0.5m 이동 후 새 노드 추가
    minimum_travel_heading: 0.5      # 0.5rad 회전 후 새 노드 추가
    scan_buffer_size: 10
    scan_buffer_maximum_scan_distance: 10.0
    link_match_minimum_response_fine: 0.1
    link_scan_maximum_distance: 1.5
    loop_search_maximum_distance: 3.0
    do_loop_closing: true
    loop_match_minimum_chain_size: 10
    loop_match_maximum_variance_coarse: 3.0
    loop_match_minimum_response_coarse: 0.35
    loop_match_minimum_response_fine: 0.45
    correlation_search_space_dimension: 0.5
    correlation_search_space_resolution: 0.01
    correlation_search_space_smear_deviation: 0.1
    loop_search_space_dimension: 8.0
    loop_search_space_resolution: 0.05
    loop_search_space_smear_deviation: 0.03
    distance_variance_penalty: 0.5
    angle_variance_penalty: 1.0
    fine_search_angle_offset: 0.00349
    coarse_search_angle_offset: 0.349
    coarse_angle_resolution: 0.0349
    minimum_angle_penalty: 0.9
    minimum_distance_penalty: 0.5
    use_response_expansion: true
    scan_queue_size: 50
    qos_overrides./scan.reliability: best_effort
```

<img width="999" height="218" alt="image" src="https://github.com/user-attachments/assets/88799120-28ea-4e0e-9d35-2d0ee26127d7" />



