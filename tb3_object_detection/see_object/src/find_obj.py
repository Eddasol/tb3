#This code recognizes objects and takes a picture of it and save it in a map on turtlebot3
#I made a variabel called "last" that saves the last object being captured so that the camera will only take picture of the object if it is different from the last object seen. This is to avoid taking endless pictures of the same object, but only one picture instead.  

#Using CvBridge for converting ROS images to OpenCV images and using OpenCV2 tutorial for saving images
#links for more info:
# http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

#For this code to work you need to install the find_object_2d package.
#Follow the installation guide in this link https://github.com/introlab/find-object 
#Use this link http://wiki.ros.org/find_object_2d for more information on how it works. This package launches the find_object application, which is where you upload pictures of objects that you want the robot to recognize. This package is being runned in the launch file.

#The camera image needs to be converted from compressed to raw format. 
#install image_transport package from https://github.com/ros-perception/image_common and run:

#You also need to install and run the camera on the turtlebot. Link for installing: #http://emanual.robotis.com/docs/en/platform/turtlebot3/appendix_raspi_cam/
#After installing run the following command on turtlebot:
#roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch

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

#set last = 0 as initial value
last = 0 

#Function that reads the topic "objects" from find_object_2d package, which prints everytime an object is deteted and which object it is
def print_object_nr(msg):
    data_array = msg.data
    if len(data_array) == 0:
	# No object detected
	i = 0
	#print('No object')
    else:
        object_number = int(data_array[0])
	print("Object number {} is detected".format(object_number))

        #defining a global variable called "newest" to be able to compare the object seen with the object seen before
        global newest 
        newest = format(object_number)

	global new_object
	new_object = True


new_object = False
newest = 0


#Function to capture image everytime a new object is detected
def save_image(msg):

    global new_object
    global last	
    #return if an object is not seen
    if not new_object:
	return
    new_object = False
    #compare newst object with the last one. If the new object is different from the last one then convert image message and save image. 
    if newest != last:
        try:    
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError, e:
            print(e)
        else:
 
            print("Saved image!")
            # Save your OpenCV2 image as a jpeg 
	    image_name = "/home/student/catkin_ws/src/tb3/tb3_object_detection/see_object/images/object" + str(newest)+".jpg"
            cv2.imwrite(image_name, cv2_img)
            #store object nr to compare with new one 
            last = newest
	    # make sound

	    sound_msg = Sound()
	    sound_msg.value=0
            sound_pub.publish(sound_msg)

   


if __name__ == '__main__':
    rospy.init_node('object_printer')

    #subscribe to the topic "objects" to print object number
    rospy.Subscriber("objects", Float32MultiArray, print_object_nr)
    #subscribe to the topic "raspicam_node/image to capture and save image"
    rospy.Subscriber("/raspicam_node/image", Image, save_image)
    #publish sound from topic "sound"
    sound_pub = rospy.Publisher('sound', Sound, queue_size=10)


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
