#!/usr/bin/env python
import roslib
import rospy
import actionlib
import json
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from rospy import loginfo as rosinfo
from time import sleep


should_send = True 
SUCCESS = 3
SELF_PRIORITY = 1
NO_PRIORITY = -1


def check_state(msg):
    loaded_dictionary = json.loads(msg.data) 
    global should_send
    pri = loaded_dictionary['priority']
    if pri == SELF_PRIORITY:# If already conrolling 
	should_send = False
    elif should_send and pri == NO_PRIORITY): #or already at goal position
	should_send = False
	# Change goal position ....
    else:
	should_send = True

if __name__ == '__main__':
    rospy.init_node('patrol_goals')
    pub = rospy.Publisher('patrol_goal', MoveBaseGoal, queue_size=10)
    rospy.Subscriber("goal_control_state", String, check_state)

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 1
    goal.target_pose.pose.position.y = 0
    goal.target_pose.pose.orientation.w = 1.0

    while not rospy.is_shutdown():
	if should_send:
	    pub.publish(goal)
	sleep(1)
