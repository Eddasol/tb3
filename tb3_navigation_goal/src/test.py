#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
from std_msgs.msg import String


current_goal_index = 0 
patrol_coord = []


def init_patrol_coord():
    if len(sys.argv) <= 1:
	filepath = "office_room.txt"
    else:
	name = sys.argv[1]
	filepath = name
    
    path = "office_room_corners.txt"
    file_corners = open(filepath, 'r')
    file_content = file_corners.read()
    file_array  = file_content.split('\n')
    coord = []
    for line in file_array:
	xy = line.split(' ')
	coord.append(xy)

    global patrol_coord 
    patrol_coord = coord


def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
	current_goal = str(patrol_coord[current_goal_index])
	msg = "Current goal is " + current_goal
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()
	global current_goal_index
	current_goal_index = (current_goal_index + 1) % len(patrol_coord)

if __name__ == '__main__':
    init_patrol_coord()
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
