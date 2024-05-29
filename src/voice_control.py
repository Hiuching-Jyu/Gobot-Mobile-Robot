import rospy
from std_msgs.msg import Bool
import os
from pydub import AudioSegment
from pydub.playback import play

# 设置标志位
#audio_played = False

def audio_signal_callback(msg):
    global audio_played
    #if msg.data and not audio_played:
        #audio_played = True  # 设置标志位，防止重复播放
    sound = AudioSegment.from_wav("/mnt/voice_share/test1.wav")
    print("Load sound done")
    play(sound)
    print("Play sound done")
    #elif not msg.data:
        #print("No message found")

def listener():
    rospy.init_node('audio_subscriber', anonymous=True)
    print("Node initialization done...")
    rospy.Subscriber('audio_signal', Bool, audio_signal_callback)
    print("Node subscription done...")
    rospy.spin()

if __name__ == '__main__':
    listener()

