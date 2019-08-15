#!/usr/bin/env python
import roslib
import rospy
import actionlib
import json
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from rospy import loginfo as rosinfo
from time import sleep

''' Sends a sequence of goals to "patrol_goal" '''

## CONSTANTS ##
SUCCESS = 3
SELF_PRIORITY = 1
NO_PRIORITY = -1

# Example goals
house_indoor_goals = [[3, 0.5, 5], [1.5, 1.3, 1], [6.5, 4, 1], [6, -4.5, 1], [-1, 4, 1], [-6.7, 4, 1], [-6, -3, 1], [-4, 1, 1]]
house_outdoor_goals = [[1, -1, 0.1], [4, -1, 0.2], [4, -6, 0.3], [8, -6, 0.4], [8, 6, 0.5], [-8, 6, 0.6], [-8, -5, 0.7], [-4, -5, 0.8], [-4, -1, 0.9], [1, -1, 1]]
example_goals = [[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]

## Global variables ##
patrol_goals = house_indoor_goals # [[x0, y0, w0], [x1, y1, w1], ... ]
should_send = True 
current_goal_index = -1
goal = None


def set_next_xy_goal():
    global goal
    global current_goal_index
    current_goal_index = (current_goal_index + 1)%len(patrol_goals)
    goal.target_pose.pose.position.x = patrol_goals[current_goal_index][0]
    goal.target_pose.pose.position.y = patrol_goals[current_goal_index][1]
    goal.target_pose.pose.orientation.w = patrol_goals[current_goal_index][2]


def check_state(msg):
    loaded_dictionary = json.loads(msg.data) 
    global should_send
    pri = loaded_dictionary['priority']
    state = loaded_dictionary['state']
    if state==SUCCESS and pri == SELF_PRIORITY:  # or already at goal position
	should_send = True
	set_next_xy_goal()
    elif pri == SELF_PRIORITY:  # If already conrolling 
	should_send = False
    else:
	should_send = True


if __name__ == '__main__':
    rospy.init_node('patrol_goals')
    pub = rospy.Publisher('patrol_goal', MoveBaseGoal, queue_size=10)
    rospy.Subscriber("goal_control_state", String, check_state)

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    set_next_xy_goal()

    while not rospy.is_shutdown():
	if should_send:
	    print('Publishing goal x:', goal.target_pose.pose.position.x, 'y:',  goal.target_pose.pose.position.y, 'theta:', goal.target_pose.pose.orientation.w)
	    pub.publish(goal)
	sleep(1)
