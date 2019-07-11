#!/usr/bin/env python
import roslib
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
#from rospy.Time import now
from rospy import loginfo as rosinfo
roslib.load_manifest('turtlebot3_nav_goal')



if __name__ == '__main__':
    rospy.init_node('simple_navigation_goals')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    while(not client.wait_for_server(rospy.Duration.from_sec(5.0))):
        rosinfo("Waiting for the move_base action server to come up")

    rosinfo("Connected")


    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 6
    goal.target_pose.pose.position.y = -5
    goal.target_pose.pose.orientation.w = 1.0

    rosinfo("Sending goal")
    client.send_goal(goal)
    client.wait_for_result()

    if (client.get_state() == actionlib.GoalStatus.SUCCEEDED):
        position = "("+str(goal.target_pose.pose.position.x)+","+str(goal.target_pose.pose.position.y)+")"
        rosinfo("Hooray, the base moved to position"+ position)
    else:
        rosinfo("The base failed to move forward 1 meter for some reason")