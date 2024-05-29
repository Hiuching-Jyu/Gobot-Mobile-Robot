# GoBot Mobile Robot
- ** This README will be updated further, please refer to https://github.com/Hiuching-Jyu/Gobot-Mobile-Robot for latest updates**
- ** Please follow the MIT license when you try to copy or apply this repository in your project.**

## 0. Hardware Configuration
- Controller: Jetson Nano B01 from Hiwonder, instruction refer to https://drive.google.com/drive/folders/1GBiwRRy0NYdtOc2z0U2wGOYut7UGFls6
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
```bash
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
```

## Overall Setup
Please run the code on your personal computer and make sure they are connected to the same Wifi because I set ROS_MASTER in Gobot, which is for PC and Gobot to share their topics published and subscribed.
```bash
roscore
```

If you don't need it, just delete the following lines in ~/.bashrc
```bash
export ROS_MASTER_URI=http://172.20.10.3:11311
export ROS_IP=172.20.10.2
```

## 5. IMU Setup
IMU documents -- wit_ros_ws/
Control file: wit_imu.launch. To run:
```bash
roslaunch wit_ros_ws imu wit_imu.launch
```

## 6. Lidar Setup
Lidar documents -- ydlidar_ws/
Control file: X3.launch
```bash
roslaunch ydlidar_ws X3.launch
```

## 7. Human following program
```
python3 humanfollow.py
roslaunch ydlidar_ws X3.launch
python3 ROS_Control.py
```
The Gobot can follow movement of human, turn left when the centre of the human is on the left-hand side, stop when a human is within 1.5 meters, move forward when people is walking in front.

## 8. Mapping
Launch the mapping file:
```bash
roslaunch hector_mapping all_node.launch
```

Use the teleoperation to control the Gobot to move around and do mapping stuff.
```bash
rosrun rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```
Save the map with map_server
```bash
rosrun map_server map_saver -f /maps/<name-of-yourmap>
```

## 9. Navigation
Change the name of the map you want to do navigation in the file named _amcl_activate.launch_, and do navigation task
```bash
roslaunch amcl amcl_activate.launch
```
The amcl_activate file includes the launch file of all sensors needed, the map server, the amcl module, the tf transform and move_base module. If you need more information on tf transform calculation please contact me by email.

However, due to some issues, the navigation module is not working right now.

## 10. Voice interaction
The Xunfei SDK does not work on ARM systems, so the voice interaction module needs an X86 PC to be the medium. Here I apply speech-to-text and voice recognition on an X86 PC, then pass the generated WAV file to the NFS system which could be reached by Jetson Nano in the same local net.

Please change all the path names in the program with your setting, and the license from Xunfei platform, since our license would be ended in 2024 July.

Run the following command on X86 PC
```bash
roscore
roslaunch robot_voice voice_assistant.launch
```
Please remember to activate the NFS system, and mount the NFS system on PC and Jetson nano, which is not provided here.
Could be like this:
```
sudo mount -t nfs <your PC IP>:<your PC document you want to share> mnt/voice_share -o rw
# For example
sudo mount -t nfs 172.20.10.3:/home/hiuching-g/A_Workspace/src/robot_voice/voice_output /mnt/voice_share -o rw
```

Maybe you should install _aplay_ on your computer, and the voice interaction program is not working well right now(it used to, believe me!). It is just a basic logic of interaction.
Run the following command on Jetson Nano
```bash
python3 voice_control.py
```
