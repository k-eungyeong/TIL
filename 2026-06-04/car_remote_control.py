import cosysairsim as airsim
import time

client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)

car_controls = airsim.CarControls()

# 전진
print("전진 중...")
car_controls.throttle = 0.6
client.setCarControls(car_controls)
time.sleep(3)
print(f"속도: {client.getCarState().speed:.2f} m/s")

# 좌회전
print("좌회전 중...")
car_controls.steering = -0.5
client.setCarControls(car_controls)
time.sleep(2)

# 직진 가속
print("전진 중...")
car_controls.throttle = 0.9
car_controls.steering = 0
client.setCarControls(car_controls)
time.sleep(4)

# 우회전
print("우회전 중...")
car_controls.steering = 0.2
client.setCarControls(car_controls)
time.sleep(1)

# 정지
print("정지 중...")
car_controls.throttle = 0
car_controls.brake = 1
car_controls.steering = 0
client.setCarControls(car_controls)

# 완전 정지 확인
while client.getCarState().speed > 0.1:
    time.sleep(0.1)

client.enableApiControl(False)
print("완료!")
