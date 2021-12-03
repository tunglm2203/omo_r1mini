#!/usr/bin/env python

import sys
import rospy
import math
from time import sleep

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

from omo_r1mini_bringup.srv import Onoff, OnoffResponse
from omo_r1mini_bringup.srv import SaveColor, ColorResponse
from omo_r1mini_bringup.srv import Battery


class TeleopJoyNode:
    def __init__(self):
        self.timer = 0
        self.auto_mode = False
        self.headlight_on = False
        self.colorIdx = 0
        self.colors = [ [255, 0, 0], [255,50, 0], [255,255,0], [0,255,0], 
            [0,0,255], [0,5,255], [100,0,255], [255,255,255] ]
        self.max_fwd_vel = rospy.get_param("~max_fwd_vel") #OMO_R1mini_MAX_LIN_VEL = 1.20
        self.max_rev_vel = rospy.get_param("~max_rev_vel")
        self.max_ang_vel = rospy.get_param("~max_ang_vel") #OMO_R1mini_MAX_ANG_VEL = 1.80
        rospy.Subscriber("/joy",  Joy, self.cb_joy, queue_size=1)
        self.pub_twist = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
        
        rospy.Timer(rospy.Duration(0.05), self.timer_update)
        self.twist = Twist()

    def cb_joy(self, joymsg):
        if self.auto_mode == False:
            if joymsg.buttons[2] == 1:
                self.auto_mode = True
                rospy.loginfo("AUTO MODE ON")
        else:
            if joymsg.buttons[2] == 1:
                self.auto_mode = False
                rospy.loginfo("AUTO MODE OFF")
        if joymsg.axes[1] > 0.0:
            self.twist.linear.x = joymsg.axes[1] * self.max_fwd_vel
        elif joymsg.axes[1] < 0.0:
            self.twist.linear.x = joymsg.axes[1] * self.max_rev_vel
        else:
            self.twist.linear.x = 0.0
        if joymsg.buttons[0] == 1:
            if self.headlight_on == False:
                self.headlight_on = True
                self.set_headlight_onOff(True)
            else:
                self.headlight_on = False
                self.set_headlight_onOff(False)

        if joymsg.buttons[3] == 1:
            rospy.loginfo("Color Set: %s, %s, %s", self.colors[self.colorIdx][0], self.colors[self.colorIdx][1],self.colors[self.colorIdx][2])
            self.set_ledColor(self.colors[self.colorIdx][0], self.colors[self.colorIdx][1],self.colors[self.colorIdx][2])
            self.colorIdx += 1
            if self.colorIdx == len(self.colors):
                self.colorIdx = 0

        self.twist.linear.y = 0.0; 
        self.twist.linear.z = 0.0
        self.twist.angular.x = 0.0; 
        self.twist.angular.y = 0.0; 
        self.twist.angular.z = joymsg.axes[0] * self.max_ang_vel

    # Service call 
    def set_headlight_onOff(self, headOnOff):
        rospy.wait_for_service('set_headlight')
        try:
            srv_headOnOff = rospy.ServiceProxy('/set_headlight', Onoff)
            OnoffResponse = srv_headOnOff(headOnOff)

        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
    
    def set_ledColor(self, red, grn, blu):
        rospy.wait_for_service('save_led_color')
        try:
            srv_saveLedColor = rospy.ServiceProxy('/save_led_color', SaveColor)
            SaveColorResponse = srv_saveLedColor(red, grn, blu)

        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

    def timer_update(self, event):
        self.timer+=1
        if self.auto_mode == False:
            self.pub_twist.publish(self.twist)

    def main(self):
        rospy.spin()


if __name__ == '__main__':
    try :
        rospy.init_node('teleop_joy_node')
        node = TeleopJoyNode()
        node.main()
    except rospy.ROSInterruptException:
        pass