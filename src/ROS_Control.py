# transfer cmd_vel to base controller
import rospy
import time
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan, Imu
from nav_msgs.msg import Odometry
import hiwonder
import math
from ackermann_msgs.msg import AckermannDriveStamped
from ackermann_msgs.msg import AckermannDrive

class RobotController:
    def __init__(self):
        # 初始化节点
        rospy.init_node('chasis_move', anonymous=True)

        # 订阅必要的主题
        self.cmd_vel_subscriber = rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)

        # 设置PWM控制舵机
        self.servo_forward = hiwonder.pwm_servo1
        self.servo_turn = hiwonder.pwm_servo2
        self.control_motor_and_servo()

        rospy.loginfo('Navigation Begin')
        time.sleep(1.0)

        # 导航目标发布者
        self.navigation_goal_publisher = rospy.Publisher('/goal_pose', PoseStamped, queue_size=10)

        # 初始化当前位置和导航目标
        self.current_pose = None
        self.navigation_goal = PoseStamped()

    def convert_trans_rot_vel_to_steering_angle(self, v, omega, wheelbase):
        if omega == 0 or v == 0:
          return 0

        radius = v / omega
        return math.atan(wheelbase / radius)

    def control_motor_and_servo(self):
        # 设置舵机参数
        self.servo_turn.deviation = 76
        self.servo_turn.max_position = 30
        self.servo_turn.min_position = -30

        self.servo_forward.deviation = 80
        self.servo_forward.max_position = 30
        self.servo_forward.min_position = -30

    def cmd_vel_callback(self, msg):
        global wheelbase
        global ackermann_cmd_topic
        global frame_id
        global pub
        global message_type
        # 解析速度和角速度
        wheelbase=1.0
        #if message_type == 'ackermann_drive':
        v = msg.linear.x
        steering = self.convert_trans_rot_vel_to_steering_angle(v, msg.angular.z, wheelbase)
    
        # 根据速度设定舵机位置
        # 假设linear_speed和angular_speed的范围为[-1, 1]，舵机的范围为[-30, 30]
        forward_position = v * 8
        turn_position = steering * 25

        # 控制舵机到指定位置
        self.servo_forward.set_position(int(forward_position),0.1)
        self.servo_turn.set_position(int(turn_position),0.1)

        rospy.loginfo('Setting forward to %s and turn to %s', forward_position, turn_position)

	
    # 其他回调函数（略）

if __name__ == '__main__':
    try:
        robot_controller = RobotController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

