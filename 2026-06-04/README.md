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
 - MS AirSim (자동차, 드론 등 대상) 
   * Cosys-AirSim : 3D 자동차, 드론 시뮬레이터, Unreal Engine 5.5버전
   * Unreal Engine의 에디터 - VS Studio 2022하고 연동돼서 C++ 코딩할 때 필요
   * 프로젝트 컴파일 및 패키징 : 지원하는 환경) Blocks.exe
   * Blocks 환경 실행 : 다수 개의 블럭 존재 + 자동차 주행 가능(키보드 조작)
   * 외부 접속을 위한 API 서버 존재
   * API 서버에 조작 명령을 전달하여 자동차 제어가 가능함
   * Cosys-AirSim 서버에 접속하고 조작하기 위한 Python 모듈이 존재
   * 결론 : Python을 사용하여 Cosys-AirSim 자동차 제어 가능
   * Cosys-AirSim 자동차에 부착된 모든 센서의 값을 API 서버를 통해 가져올 수 있음 = 센서 값을 가져와서 ROS2 돌릴 수 있고 ~ 위 주 영역 부분 단계!
   * airsim_ros_pkgs 을 설치하면 Cosys-AirSim 과 ROS2 를 쉽게 연동 가능 
     ⇒ ROS2 → airsim_ros_pkgs를 이용해서 → Cosys-AirSim 제어 가능 → ROS2에 센서의 값 전달 가능

  Cosys-AirSim, Unreal Engin 5.5, VS Stuido 2022, Python, ROS2 
- ROS2로 들어가자면, 필요로 하는 OS는 리눅스임! 
  * Linux OS에 ROS2 설치 필요 (Linux(Ubuntu 22.04버전 권장)
  * WSL(Windows Subsystem for Linux)를 이용하면 윈도우 안에 리눅스 설치 가능함 

✅ AI 개발/ 실행이 Python에서 Linux로 넘어가야 함!
    - Windows 기반에서 Cosys-AirSim 실행
    - Linux 기반에서 ROS2, Python, AI 실행 

  Cosys-AirSim 실행 환경
- Win 10, 11 / RAM 16GB 이상 / 저장 공간 100GB 이상


##### [ 3교시 ]  

<img width="564" height="101" alt="image" src="https://github.com/user-attachments/assets/894ab28a-4d33-4379-a1fe-639ce371e3f7" />

##### [ 4교시 ]  

<img width="642" height="147" alt="image" src="https://github.com/user-attachments/assets/f87c3167-f17c-4d79-b4d6-fbf0c8353435" />
<img width="671" height="115" alt="image" src="https://github.com/user-attachments/assets/57f8f954-733c-41cf-b23d-0b16097fc2a5" />

##### [ 5교시 ]  
Blocks 환경 업데이트
Developer Command Prompt에서 실행:
cd C:\Cosys-AirSim\Unreal\Environments\Blocks\
위의 경로에서 실행 -> update_from_git.bat

##### [ 7교시 ]  


### 어려웠던 점
### 느낀 점
