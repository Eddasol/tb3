#!/usr/bin/env python
import json
import rospy
import sys, select, os
from move_base_msgs.msg import MoveBaseGoal
from std_msgs.msg import String

''' Takes in user input and sents goal to "user_input" topic '''


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


def print_dictionary(msg):
    loaded_dictionary = json.loads(msg.data)



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


def retreive_number(end_key=' '):
    number = 0
    num_decimals = -1
    sign = 1
    while not rospy.is_shutdown():
        key = getKey()
        if is_int(key):
            if num_decimals == -1:
                number = number*10 + int(key)
            else:
                num_decimals += 1
                number += int(key)*10**(-(num_decimals))
        elif key == '.':
            num_decimals = max(num_decimals, 0)
        elif key == '-':
            sign = -1
        elif key == end_key:
            break
        else:
            continue
        print(sign*number)
    return sign*number


def get_and_transmit_corrdinates(pub):
    '''
    Asks for user input and transmits the received goal to pub
    '''
    status = 0
    try:
        print msg
        while not rospy.is_shutdown():
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

    finally:

        # Upon exit it goes back to predecides position (ex: charging station)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = -3
        goal.target_pose.pose.position.y = 1
        goal.target_pose.pose.orientation.w = 1.0
        pub.publish(goal)



if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('user_input')
    pub = rospy.Publisher('user_input', MoveBaseGoal, queue_size=10)
    rospy.Subscriber("goal_control_state", String, print_dictionary)
    get_and_transmit_corrdinates(pub)


    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
