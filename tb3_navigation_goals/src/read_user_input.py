#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseGoal

import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios


msg = """
Control Your TurtleBot3!
---------------------------
n to choose new desired position
"""

e = """
Communications Failed
"""

def is_int(num):
    try:
        int(num)
        return True
    except:
        return False

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

settings = None
def init_key_input():
    global settings
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)


def end_key_input():
    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

def retreive_number(end_key=' '):
    number = 0
    num_decimals = -1
    while(1):
        key = getKey()
        if is_int(key):
            if num_decimals == -1:
                number = number*10 + int(key)
            else:
                num_decimals += 1
                number += int(key)*10**(-(num_decimals))
        elif key == end_key:
            break
        elif key == '.':
            num_decimals = max(num_decimals, 0)
        elif key == '\x03':
            break
        else:
            continue
        print(number)
    return number

def get_and_transmit_corrdinates(pub):
    '''
    Asks for user input and transmits the received goal to pub
    '''
    status = 0
    try:
        print msg
        while(1):
            key = getKey()
            if key == 'n':
                # Get desired x, y position and publishes the coordinates
                status = 1

                print("Enter desired x position followed by space")
                x = retreive_number()
                print("Enter desired y position followed by space")
                y = retreive_number()

                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = x
                goal.target_pose.pose.position.y = y
                goal.target_pose.pose.orientation.w = 1.0
                pub.publish(goal)
            elif (key == '\x03'):
                break

            if status:
                print msg
                status = 0

    except:
        print e


if __name__=="__main__":
    init_key_input()

    rospy.init_node('turtlebot3_navigation_goals')
    pub = rospy.Publisher('goals', MoveBaseGoal, queue_size=10)
    get_and_transmit_corrdinates(pub)
    end_key_input()


