#!/usr/bin/env python 
# import rospy 
# from sensor_msgs.msg import Image 
# from cv_bridge import CvBridge, CvBridgeError 
# from std_msgs.msg import String
import cv2 
import numpy as np
from pandas import DataFrame
#bridge_object = CvBridge() # create the cv_bridge object 

class hsv():
    def __init__(self):
        self.center = [0, 0]
        self.image_received = 0 #Flag to indicate that we have already received an image 
        self.cv_image = 0 

        #rospy.Subscriber("/iris_0/usb_cam/image_raw", Image, self.camera_callback) 


    def process_image(self, image):

        image = cv2.resize(image,(640,360)) 
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

        r_lower = np.array([175,128, 61])
        r_upper = np.array([255, 255, 255])
        # r_lower = np.array([0, 0, 0])
        # r_upper = np.array([0, 0, 255])
        r_mask = cv2.inRange(hsv, r_lower, r_upper)
        #erode
        kernal1 = np.ones((5, 5), "uint8")
        erode_img=cv2.erode(r_mask,kernal1)
        #dilate
        kernal2 = np.ones((11, 11), "uint8")
        final=cv2.dilate(erode_img,kernal2)
        cv2.imshow(final)
        #r_mask, contours, hierarchy = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)###old
        contours, hierarchy = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)###new
        if type(hierarchy) == np.ndarray:

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    p = x + (w//2)
                    q = y + (h//2)
                    self.center = [p, q]
                    center = self.center
                    Target = 'Target:'+str(self.center)
                    cv2.putText(image, Target, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                    print('target=',Target)
                            #self.center = rospy.center()
                    
                    #if (q>80):
                        #print('Target', self.center)
                        #print("Number of Contours found = " + str(len(contours)))

        else:
            self.center = [None, None]
            self.area = None
            # print('No target')
            # print('u,v =', self.center)

        cv2.imshow("detection", image)
        cv2.imwrite("detection.jpg", image)
        cv2.waitKey(1)
        return center 
        
    def camera_callback(self, data): 
 
        self.image_received=1 
        try: 
            #print("received ROS image, I will convert it to opencv") 
            # We select bgr8 because its the OpenCV encoding by default 
            self.cv_image = bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8") 
            #Add your code to save the image here: 
            #Save the image "img" in the current path  
            #cv2.imwrite('uav_image.jpg', self.cv_image)        
            ## Calling the processing function
            self.process_image(self.cv_image)
            #cv2.imshow('Image from uav camera', self.cv_image) 

        except CvBridgeError as e: 
            print(e) 

    def value_callback(self):
        center_position = self.center
        return center_position

    def iteration(self,event):
        pass
        # print('center = ')
        # print(self.center)
        

if __name__ == '__main__': 
    rospy.init_node('hsv', anonymous=True) 
     
    dt = 1.0/20
    pathplan_run = hsv()
    rospy.Timer(rospy.Duration(dt), pathplan_run.iteration)
    rospy.spin()