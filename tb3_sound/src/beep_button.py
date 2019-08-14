#!/usr/bin/env python
''' Alternates between on and off sound '''
import rospy
from turtlebot3_msgs.msg import Sound

def talker():
    pub = rospy.Publisher('sound', Sound, queue_size=10)
    rospy.init_node('talker')
    rate = rospy.Rate(0.2) # 4hz
    toggle = 0
    while not rospy.is_shutdown():
	msg = Sound()
	if toggle:
		msg.value=0
		toggle = 0
	else:
		msg.value=1
		toggle = 1
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

