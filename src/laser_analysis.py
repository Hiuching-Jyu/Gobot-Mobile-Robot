#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
import numpy as np
import os

class LidarDistanceMonitor:
    def __init__(self, target_angles_degrees, save_dir):
        rospy.init_node('lidar_distance_monitor', anonymous=True)
        self.target_angles = target_angles_degrees  # Keep angles in degrees
        self.distances = {angle: [] for angle in target_angles_degrees}
        self.timestamps = []

        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        self.rate = rospy.Rate(10)  # 10Hz

    def laser_callback(self, data):
        angle_min = data.angle_min
        angle_max = data.angle_max
        angle_increment = data.angle_increment

        timestamp = rospy.Time.now().to_sec()
        self.timestamps.append(timestamp)

        for angle in self.target_angles:
            target_angle_rad = angle * (np.pi / 180.0)  # Convert degrees to radians
            target_index = int((target_angle_rad - angle_min) / angle_increment)
            if 0 <= target_index < len(data.ranges):
                distance = data.ranges[target_index]
            else:
                distance = float('inf')  # Use inf if the index is out of range
            self.distances[angle].append(distance)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

    def plot_distances(self):
        for angle in self.distances:
            if len(self.timestamps) == len(self.distances[angle]):  # Ensure dimensions match
                plt.figure()
                plt.plot(self.timestamps, self.distances[angle], label=f'Distance at {angle} degrees')
                plt.xlabel('Time (s)')
                plt.ylabel('Distance (m)')
                plt.title(f'Distance Change at {angle} Degrees')
                plt.legend()
                plt.savefig(os.path.join(self.save_dir, f'distance_{angle}_degrees.png'))
                plt.close()
            else:
                print(f"Data length mismatch for angle {angle} degrees")

if __name__ == '__main__':
    target_angles_degrees = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    save_dir = './lidar_plots'  # Directory to save the plots

    monitor = LidarDistanceMonitor(target_angles_degrees, save_dir)

    try:
        monitor.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        monitor.plot_distances()

