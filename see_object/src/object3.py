#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray

def print_object_nr(msg):
    data_array = msg.data
    if len(data_array) == 0:
	# No object detected
	print('No object')
    else:
	object_number = int(data_array[0])
	print("Object number {} is detected".format(object_number))
    

if __name__ == '__main__':
    rospy.init_node('object_printer', anonymous=True)

    rospy.Subscriber("objects", Float32MultiArray, print_object_nr)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
