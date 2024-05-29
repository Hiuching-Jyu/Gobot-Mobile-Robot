#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import cv2
import mediapipe as mp

class AutoFollower:
    def __init__(self):
        rospy.init_node('auto_follower', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)  # 10Hz
        self.distance = float('inf')  # Initialize distance as infinite

        # Subscribe to the laser scan topic
        rospy.Subscriber('/scan', LaserScan, self.laser_callback)

        # MediaPipe initialization
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils  # Used to draw the landmarks

    def laser_callback(self, data):
        # Process laser scan data to find the closest object in the specified range (120 to 240 degrees)
        ranges = data.ranges
        angle_min = data.angle_min
        angle_max = data.angle_max
        angle_increment = data.angle_increment

        # Calculate the start and end indices for the 120 to 240 degree range
        start_angle = 150.0 * (3.14159 / 180.0)  # Convert degrees to radians
        end_angle = 210.0 * (3.14159 / 180.0)  # Convert degrees to radians
        start_index = int((start_angle - angle_min) / angle_increment)
        end_index = int((end_angle - angle_min) / angle_increment)

        valid_ranges = [r for r in ranges[start_index:end_index] if data.range_min < r < data.range_max]

        if valid_ranges:
            self.distance = min(valid_ranges)
        else:
            self.distance = float('inf')
        print(self.distance)

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        # Draw landmarks on the frame
        self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        if results.pose_landmarks:
            nose_landmark = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            move_cmd = Twist()

            if nose_landmark.x < 0.4:
                move_cmd.angular.z = 0.8  # Turn left
            elif nose_landmark.x > 0.6:
                move_cmd.angular.z = -0.8  # Turn right

            if self.distance > 1.5:  # Move forward if the person is more than 1 meter away
                move_cmd.linear.x = 0.5  # Move forward proportional to the distance, max speed 1.0
            else:  # Stop or keep a safe distance
                move_cmd.linear.x = 0.0

            self.pub.publish(move_cmd)
        else:
            move_cmd.linear.x = 0.0
            self.pub.publish(move_cmd)

        # Display the processed frame
        cv2.imshow('MediaPipe Pose', frame)
        cv2.waitKey(1)  # Pause briefly to update the display

    def run(self):
        cap = cv2.VideoCapture(0)
        while not rospy.is_shutdown():
            ret, frame = cap.read()
            if ret:
                self.process_frame(frame)
            self.rate.sleep()

if __name__ == '__main__':
    follower = AutoFollower()
    try:
        follower.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        cap.release()  # Release the camera resource
        cv2.destroyAllWindows()  # Close all OpenCV windows

