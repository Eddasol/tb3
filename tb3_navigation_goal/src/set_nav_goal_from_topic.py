#!/usr/bin/env python
import roslib
import rospy
import actionlib
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from std_msgs.msg import String
from threading import Semaphore
from rospy import loginfo as rosinfo
from time import time as Time

''' Sends the goal in "user_input" topic to move_base '''

client = None
state = "normal"
available_goal = Semaphore(value=0)	


def callback(goal):
    global available_goal

    # sets a new timestamp, but otherwise sends the same message
    goal.target_pose.header.stamp = rospy.Time.now()
    rosinfo("Sending new goal (%s, %s)", goal.target_pose.pose.position.x, goal.target_pose.pose.position.y)
    client.send_goal(goal)

    available_goal.release()


if __name__ == '__main__':
    # Initializing
    rospy.init_node('set_nav_goal')
    rospy.Subscriber("user_input", MoveBaseGoal, callback)
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)


    # Wait for connection
    while (not client.wait_for_server(rospy.Duration.from_sec(5.0))) and not rospy.is_shutdown():
        rosinfo("Waiting for the move_base action server to come up")
    rosinfo("Connected")

    # Give feedback to user
    while not rospy.is_shutdown():
        available_goal.acquire()
	if rospy.is_shutdown():
		break
        client.wait_for_result()

        if (client.get_state() == actionlib.GoalStatus.SUCCEEDED):
            rosinfo("Hooray, the base moved to the goal position")
        else:
            rosinfo("The base failed to move to the goal position for some reason")
