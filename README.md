# GoBot Mobile Robot

## 1. General Notes
- **Username:** hiwonder
- **Password:** hiwonder
- **Battery:** 38 (low), 42 (full)
- **Remote Control Adjustment Knobs:**
  1. Basic rotation angle of the wheel
  2. Power level: adjust until it moves, then to max, then until motor sound
  3. Rotation amplitude
  4. Not remembered
- **Button Functions:**
  - Green: lights
  - Red: front and rear drive

## 2. WIFI Settings
Follow section 6.3 in "Multi-Machine Communication Configuration" to modify the settings for connecting to WIFI. After modification, restart to auto-connect. Currently using `DengdengJyu`, password `zhuxiaoqing666`, IP address `172.20.10.3`. For more details, refer to:
- [Multi-Machine Communication Configuration](https://kdocs.cn/l/cqqSR0z9tjTq)
- [Multi-Machine Communication Configuration](https://kdocs.cn/l/cquTZzXia5yd)

If you want to connect your phone to the robot's hotspot, change a specific parameter back to 1 as described in the configuration guide and use the WonderAi app. Currently, it's not very useful, so it's better not to change it.

## 3. VNC Remote Connection
Install VNC Viewer on your computer, connect to `hiwonder`'s IP address `172.20.10.2`, and use the password `hiwonder` to view and control the Jetson Nano on a larger screen.

## 4. Inertial Navigation IMU
Control file: `imu_usb.py`. Currently ensures all sensors output information separately. To run:
```bash
python3 imu_usb.py
launch wit_ros_ws imu wit_imu.launch
