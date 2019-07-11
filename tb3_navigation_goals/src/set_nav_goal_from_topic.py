#!/usr/bin/env python
import roslib
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
#from rospy.Time import now
from rospy import loginfo as rosinfo
roslib.load_manifest('turtlebot3_nav_goal')

NO_GOAL = 0
MOVING_TO_GOAL = 1
client = None
state = NO_GOAL

def callback(goal):
    # sets a new timestamp, but otherwise sends the same message
    goal.target_pose.header.stamp = rospy.Time.now()
    rosinfo("Sending new goal (%s, %s)", goal.target_pose.pose.position.x, goal.target_pose.pose.position.y)
    client.send_goal(goal)

    global status
    status = MOVING_TO_GOAL




if __name__ == '__main__':
    # Initializing
    rospy.init_node('simple_navigation_goals')
    rospy.Subscriber("goals", MoveBaseGoal, callback)
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    # Wait for connection
    while(not client.wait_for_server(rospy.Duration.from_sec(5.0))):
        rosinfo("Waiting for the move_base action server to come up")
    rosinfo("Connected")

    # Give feedback to user
    while(1):
        global state
        while(state != MOVING_TO_GOAL):
            i = 0
            #Do nothing

        client.wait_for_result()
        state = NO_GOAL

        if (client.get_state() == actionlib.GoalStatus.SUCCEEDED):
            position = "("+str(goal.target_pose.pose.position.x)+","+str(goal.target_pose.pose.position.y)+")"
            rosinfo("Hooray, the base moved to position"+ position)
        else:
            rosinfo("The base failed to move forward 1 meter for some reason")
