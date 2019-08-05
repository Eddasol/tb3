#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, PoseWithCovariance
from std_msgs.msg import String

DORMANT = 0
ACTIVE = 1
state = DORMANT

is_desperate = False
n = 230
distance_desperate_threshold = 0.8
distance_threshold = 1.5 
max_speed_threshold = 2.5
max_speed = 1
min_speed = 0.5

speed_pub = None
start_position = None


def update_state(data):
	print("update_state")
	if data.data == "recovery":
		new_state = ACTIVE
		print('new_state', new_state)
		set_state(new_state)
		print("recovery activated")
	else:
		set_state(DORMANT)
		print("Recovery ended")


def set_state(value):
	global state
	print("value", value)
	print("state_pre", state)
	if value == DORMANT:
		start_position = None
		state = DORMANT
	if value == ACTIVE:
		print("setting_active")
		state = ACTIVE
	print("state_post", state)


def set_speed(distance):
	print("Entering 'set_distance'")
	if state == DORMANT:
		return

	speed = Twist()
	print("Current distance", distance)
	if distance > distance_threshold:
		x = max(max_speed, (max_speed-min_speed)/(max_speed_threshold-distance_threshold)*distance)
		speed.linear.x = x
		print("Forward")
	else:
		speed.angular.z = 0.8
		print("Turning")
	speed_pub.publish(speed)


def read_laser(data):
	print("state", state)
	if state == DORMANT:
		return
	front_read = [data.ranges[i] for i in range (n, len(data.ranges) - n)]
	set_speed(min(front_read))		 


def main():
    global speed_pub
    rospy.init_node('recovery')
    rospy.Subscriber("navigation_status", String, update_state) 
    rospy.Subscriber("taurob_tracker/laser_scan", LaserScan , read_laser)
    speed_pub = rospy.Publisher("taurob_tracker/cmd_vel_raw", Twist)
    rospy.spin()


if __name__ == '__main__':
    main()
