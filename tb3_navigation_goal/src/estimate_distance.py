#!/usr/bin/env python
import rospy
from math import sqrt
from nav_msgs.msg import Path


def distance(a, b):
	del_x = a.pose.position.x - b.pose.position.x
	del_y = a.pose.position.y - b.pose.position.y
	return sqrt(del_x**2 + del_y**2)


def path_distance(path, increment_gain = 5):
	index = 0
	max_index = len(path.poses) - 1 
	length = 0
	while not rospy.is_shutdown():
		if index + increment_gain < max_index:
			length += distance(path.poses[index], path.poses[index + increment_gain])
			index += increment_gain
		else: 
			length += distance(path.poses[index], path.poses[max_index])
			break
	return length

def callback(path):
	print("Acc:", path_distance(path, increment_gain = 1), "Est:",path_distance(path, increment_gain = 5))


if __name__ == '__main__':
    # Initializing
    rospy.init_node('est_dist')
    rospy.Subscriber("move_base/NavfnROS/plan", Path, callback)
    rospy.spin()
