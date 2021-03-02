#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import Int16
from ur_msgs.srv import SetSpeedSliderFraction


current_level = 1
count = 0
potential_level = 0
maximum_speed = rospy.get_param('/demonstrator_speed_control/maximum_speed')
def testInfoCallback(msg):
  global current_level
  global count
  global potential_level
  if msg == current_level:
    count = 0
    potential_level = 0
    print msg, count, current_level, potential_level
    
  else:
    if potential_level == 0:
      potential_level = msg
      count = 1
      print msg, count, current_level, potential_level
    else:
      if msg == potential_level:
        count = count + 1
        print msg, count, current_level, potential_level
        if count > 4:
          rospy.loginfo("Speed changed.")
          print potential_level

          speed_level_str = str(potential_level)
          if speed_level_str == "data: 2":
            rospy.wait_for_service('/ur_hardware_interface/set_speed_slider')
            try:
              add_SetSpeedSliderFraction = rospy.ServiceProxy('/ur_hardware_interface/set_speed_slider', SetSpeedSliderFraction)
              response = add_SetSpeedSliderFraction(0.3 * maximum_speed)
              return response.success
            except rospy.ServiceException, e:
              print "Service call failed: %s"%e

          elif speed_level_str == "data: 1":
            rospy.wait_for_service('/ur_hardware_interface/set_speed_slider')
            try:
              add_SetSpeedSliderFraction = rospy.ServiceProxy('/ur_hardware_interface/set_speed_slider', SetSpeedSliderFraction)
              response = add_SetSpeedSliderFraction(0.01)
              return response.success
            except rospy.ServiceException, e:
              print "Service call failed: %s"%e

          elif speed_level_str == "data: 1":
            rospy.wait_for_service('/ur_hardware_interface/set_speed_slider')
            try:
              add_SetSpeedSliderFraction = rospy.ServiceProxy('/ur_hardware_interface/set_speed_slider', SetSpeedSliderFraction)
              response = add_SetSpeedSliderFraction(maximum_speed)
              return response.success
            except rospy.ServiceException, e:
              print "Service call failed: %s"%e

          else:
            pass


          current_level = potential_level
          count = 0
          potential_level = 0
        else:
          pass
      else:        
        potential_level = msg
        count = 1
        print msg, count, current_level, potential_level


def speed_subscriber():
  rospy.init_node('demonstrator_speed_control')
  rospy.Subscriber("/distance_level", Int16, testInfoCallback, queue_size = 1)
  rospy.spin()

if __name__ == '__main__':
  speed_subscriber()

