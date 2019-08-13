#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
from turtlebot3_msgs.msg import Sound
# Instantiate CvBridge
bridge = CvBridge()


last = 0 
def print_object_nr(msg):
    data_array = msg.data
    if len(data_array) == 0:
	# No object detected
	i = 0
	#print('No object')
    else:
        object_number = int(data_array[0])
	print("Object number {} is detected".format(object_number))
        global newest 
        newest = format(object_number)

	global new_object
	new_object = True


new_object = False
newest = 0

def save_image(msg):

    global new_object
    global last	
    if not new_object:
	return
    new_object = False
    #compare object with the last one
    if newest != last:
        try:    
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError, e:
            print(e)
        else:
 
            print("Saved image!")
            # Save your OpenCV2 image as a jpeg 
	    image_name = "catkin_ws/src/see_object/images/object" + str(newest)+".jpg"
            cv2.imwrite(image_name, cv2_img)
            #store object nr to compare with new one 
            last = newest
	    # make sound

	    sound_msg = Sound()
	    sound_msg.value=0
            sound_pub.publish(sound_msg)

   


if __name__ == '__main__':
    rospy.init_node('object_printer')

    rospy.Subscriber("objects", Float32MultiArray, print_object_nr)
    sub = rospy.Subscriber("objects", Float32MultiArray, print_object_nr)
    rospy.Subscriber("/raspicam_node/image", Image, save_image)
    sound_pub = rospy.Publisher('sound', Sound, queue_size=10)


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
