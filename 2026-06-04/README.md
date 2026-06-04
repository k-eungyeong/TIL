# 2026-06-04
### 배운 내용
##### [ 1교시 ]  
자율 주행(Autonomous Driving, Self-Driving) - 운전자의 조작 없이 차량이 스스로 판단하고 주행하는 기술 
 [ 구성 요소 ]
  * 인지(Perception) - 위치, 주변 환경 등을 알아야 함(SW가)! 
                                       그래서 센서 필요 (ex. 실물 색상 뽑는 RGB 카메라, 주변 장애물과 거리 등 확인하는 Depth Cam, GPS, 레이저를 이용한 LiDAR, 
                                                                             IMU(방향 지시))
  * 위치추정(Localization) 
  * 판단(Planning) - 속도 몇? 핸들 언제 꺾어? 교차로 좌/우회전? 목표를 위한 최단거리는? → 네비게이션이 할 일
  * 제어(Control) - 속도(전/후진), 조향 각도
  * 통신(Communication)

 - 우리의 주 영역 : ROS2(Robot Operating System2) - 로봇을 운영하기 위한 OS
  * 센서(Camera, LiDAR, IMU) → ROS2(Robot Operating System2) → SLAM(Simultaneous Localization and Mapping) - 지도 생성 + 위치 추청
     → Nav2(Navigation2) - 경로 계획 + 장애물 회피 → 제어(조향, 가속, 제동) 

- 실무적으로 가장 많이 사용하는 AI 영역(자율주행에서)
  * 객체 인식(Object Detection) → YOLO
  * 차선 인식(Lane Detection)
  * 신호등 인식(Traffic Light Detection)
  * 보행자·차량 행동 예측(Prediction)
  * 경로 계획(Planning)
  * End-to-End 자율주행

 - MS AirSim (자동차, 드론 등 대상) 
   * Cosys-AirSim
  
##### [ 2교시 ]  


### 어려웠던 점
### 느낀 점
