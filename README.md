# GoBot Mobile Robot
## 0. Hardware Configuration
- Controller: Jetson Nno B01 from Hiwonder, instruction refer to https://drive.google.com/drive/folders/1GBiwRRy0NYdtOc2z0U2wGOYut7UGFls6
- Chasis: PWM control Ackermann chasis
- IMU: Yahboom 10-axis IMU, instruction refer to https://www.yahboom.com/study/IMU# 
- Lidar: X3 Pro, instruction refer to https://www.yahboom.com/study/YDLIDAR-X3
- Mono-Camera: HIKVISION, using USB port.
- Sound box, with a converter.
- Screen, keyboard, and mouse.


## 1. General Notes
- **Jetson Nano Username:** hiwonder
- **Jetson Nano Password:** hiwonder
- **Chasis Battery:** 38 (low), 42 (full)
- **Remote Control Handle Adjustment Knobs:**
  1. Basic rotation angle of the wheel
  2. Power level: adjust until it moves, then to max, then until motor sound
  3. Rotation amplitude
  4. Not Remembered...
     
- **Chasis Button Functions:**
  - Green: lights
  - Red: front and rear drive

## 2. WIFI Settings
Follow section 6.3 in "Multi-Machine Communication Configuration" to modify the settings for connecting to WIFI. After modification, restart to auto-connect. Currently using `DengdengJyu`, password `zhuxiaoqing666`, IP address `172.20.10.3`. For more details, refer to: https://drive.google.com/drive/folders/1GBiwRRy0NYdtOc2z0U2wGOYut7UGFls6

If you want to connect your phone to the robot's hotspot, change a specific parameter back to 1 as described in the configuration guide and use the WonderAi app. Currently, it's not very useful, so it's better not to change it.

## 3. Remote Connection From Personal Computer
- Method 1: Install VNC Viewer on your computer, connect to `hiwonder`'s IP address `172.20.10.2`, and use the password `hiwonder` to view and control the Jetson Nano on a larger screen.
- Method 2: ssh hiwonder@172.20.10.2
- Method 3: no machine, refer to https://drive.google.com/drive/folders/1GBiwRRy0NYdtOc2z0U2wGOYut7UGFls6
- Method 4: using "scp" to transfer files from Jetson Nano to Personal Computer

## 4. Installation
- sudo apt-get install ros-melodic-ackermann-msgs
- sudo apt-get install ros-melodic-random-numbers
- sudo apt-get install ros-melodic-opencv-apps
- sudo apt-get install ros-melodic-pcl-conversations
- sudo apt-get install ros-melodic-pcl-ros
- sudo apt-get install ros-melodic-hector*
- sudo apt-get install ros-melodic-amcl
- sudo apt-get install ros-melodic-map-server
- sudo apt-get install ros-melodic-move-base
- sudo apt-get install ros-melodic-teleop-twist*
follow the readme in mcskf, and install stuff from ydlidar-SDK

## 5. IMU Setup
IMU file -- wit_ros_ws
Control file: `imu_usb.py`. Currently ensures all sensors output information separately. To run:
```bash
python3 imu_usb.py
launch wit_ros_ws imu wit_imu.launch
