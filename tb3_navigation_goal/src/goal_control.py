#!/usr/bin/env python
import roslib
import rospy
import actionlib
import math
import json
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from actionlib_msgs.msg import GoalID
from std_msgs.msg import String
from rospy import loginfo as rosinfo
from time import time, sleep


## CONSTANTS ##
# Topics
LOW_BATTERY_TOPIC = "batterymodule_goal"
'''if rospy.has_param('user_input_topic'):
	USER_INPUT_TOPIC = rospy.get_param("user_input_topic") 
else:
    print("error")'''
USER_INPUT_TOPIC = "user_input"
PATROL_TOPIC = "patrol_goal"
STATE_TOPIC = "goal_control_state"
# Priorities
LOW_BATTERY_PRIORITY = 3
USER_INPUT_PRIORITY = 2
PATROL_PRIORITY = 1
NO_GOAL_PRIORITY = -1
# States
WAITING = 0
SENDING_GOAL = 1
DRIVING = 2
GOAL_SUCCESS = 3
GOAL_ABORT = 4

## Global variables ##
current_priority = -1
client = None


def send_goal(goal):
    rosinfo("Sending new goal (%s, %s)", goal.target_pose.pose.position.x, goal.target_pose.pose.position.y)
    client.send_goal(goal)


def send_state(state):
    ## state = {waiting, sending_goal, driving, goal_success, goal_abort}
    info = {"priority": current_priority, "state": state}
    encoded_data_string = json.dumps(info)
    print("Publishing:", encoded_data_string, "of type:", type(encoded_data_string))
    pub.publish(encoded_data_string)
	

def set_priority(new_priority):
    global current_priority
    current_priority = new_priority


def low_battery_callback(msg):
    if LOW_BATTERY_PRIORITY < current_priority:
	return
    set_priority(LOW_BATTERY_PRIORITY)
    send_goal(msg)
    send_state(SENDING_GOAL)


def user_input_callback(msg):
    if USER_INPUT_PRIORITY < current_priority:
	return
    set_priority(USER_INPUT_PRIORITY)
    send_goal(msg)
    send_state(SENDING_GOAL)


def patrol_callback(msg):
    if PATROL_PRIORITY < current_priority:
	return
    set_priority(PATROL_PRIORITY)
    send_goal(msg)
    send_state(SENDING_GOAL)


if __name__ == '__main__':
    # Initializing
    rospy.init_node('goal_control')

    pub = rospy.Publisher(STATE_TOPIC, String, queue_size=10)
    

    rospy.Subscriber(LOW_BATTERY_TOPIC, MoveBaseGoal, low_battery_callback)
    rospy.Subscriber(USER_INPUT_TOPIC, MoveBaseGoal, user_input_callback)
    rospy.Subscriber(PATROL_TOPIC, MoveBaseGoal, patrol_callback)
    
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)


    # Wait for connection
    while (not client.wait_for_server(rospy.Duration.from_sec(5.0))) and not rospy.is_shutdown():
        rosinfo("Waiting for the move_base action server to come up")
    rosinfo("Connected")

    # Give feedback to user
    while not rospy.is_shutdown():
	# Wait for a goal
	while current_priority == -1:
	    sleep(0.5)

        client.wait_for_result()

        if (client.get_state() == actionlib.GoalStatus.SUCCEEDED):
	    send_state(GOAL_SUCCESS)
	    set_priority(NO_GOAL_PRIORITY)
            rosinfo("Hooray, the base moved to the goal position")
        else:
	    send_state(GOAL_ABORT)
	    set_priority(NO_GOAL_PRIORITY)            
	    rosinfo("The base failed to move to the goal position for some reason")


