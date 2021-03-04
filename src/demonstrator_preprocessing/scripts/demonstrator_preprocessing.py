#!/usr/bin/env python
import rospy
import roslib
roslib.load_manifest('demonstrator_preprocessing')
import time
import math
import tf
import geometry_msgs.msg
from std_msgs.msg import Int16
import message_filters
from sensor_msgs.msg import LaserScan

class Demonstrator():
  def __init__(self):
    self.laser_front_sub = message_filters.Subscriber("laserscan_filtered/front", LaserScan)
    self.laser_rear_sub = message_filters.Subscriber("laserscan_filtered/rear", LaserScan)
    self.ts = message_filters.ApproximateTimeSynchronizer([self.laser_front_sub, self.laser_rear_sub], queue_size = 10, slop=0.5)
    self.ts.registerCallback(self.scan_callback)

    self.listener = tf.TransformListener()

    self.angle_min = -1.570796
    self.angle_max = 3.1415926
    self.sample = 811
    self.angle_increment = (self.angle_max - self.angle_min) / self.sample   
 
    self.nearest_point_range_front = 0.0
    self.nearest_point_range_rear = 0.0
    self.nearest_point_index = 0.0
    self.nearest_point_angle = 0.0
    self.nearest_point_x = 0.0
    self.nearest_point_y = 0.0
    self.nearest_point_to_chassis_x = 0.0
    self.nearest_point_to_chassis_y = 0.0
    self.nearest_point_to_chassis = 0.0

    self.ctrl_c = False
    self.rate = rospy.Rate(1)
    rospy.on_shutdown(self.shutdownhook)
	
  def scan_callback(self, laser_front, laser_rear):
    laser_front.ranges = [100 if math.isnan(x) else x for x in laser_front.ranges]
    laser_front.ranges = [100 if x < 0.1 else x for x in laser_front.ranges]
    laser_rear.ranges = [100 if math.isnan(x) else x for x in laser_rear.ranges]
    laser_rear.ranges = [100 if x < 0.1 else x for x in laser_rear.ranges]
        
    self.nearest_point_range_front = min(laser_front.ranges)
    self.nearest_point_range_rear = min(laser_rear.ranges)
    if self.nearest_point_range_front < self.nearest_point_range_rear:
      self.nearest_point_index = laser_front.ranges.index(min(laser_front.ranges))    
      self.nearest_point_angle = self.nearest_point_index * self.angle_increment + self.angle_min
      self.nearest_point_x = self.nearest_point_range_front * math.cos(self.nearest_point_angle)
      self.nearest_point_y = self.nearest_point_range_front * math.sin(self.nearest_point_angle)
    else:
      self.nearest_point_index = laser_rear.ranges.index(min(laser_rear.ranges))    
      self.nearest_point_angle = self.nearest_point_index * self.angle_increment + self.angle_min
      self.nearest_point_x = self.nearest_point_range_rear * math.cos(self.nearest_point_angle)
      self.nearest_point_y = self.nearest_point_range_rear * math.sin(self.nearest_point_angle)

  def read_laser(self):
    level_pub = rospy.Publisher('/distance_level', Int16, queue_size = 10)
    while not self.ctrl_c:
      try:
        if self.nearest_point_range_front < self.nearest_point_range_rear:
          (trans,rot) = self.listener.lookupTransform('/chassis', '/sick_front', rospy.Time(0))
          self.nearest_point_to_chassis_x = self.nearest_point_x + trans[0]
          self.nearest_point_to_chassis_y = self.nearest_point_y + trans[1]
          self.nearest_point_to_chassis = math.sqrt(self.nearest_point_to_chassis_x ** 2 + self.nearest_point_to_chassis_y ** 2)

        else:
          (trans,rot) = self.listener.lookupTransform('/chassis', '/sick_rear', rospy.Time(0))
          self.nearest_point_to_chassis_x = self.nearest_point_x - trans[0]
          self.nearest_point_to_chassis_y = self.nearest_point_y - trans[1]
          self.nearest_point_to_chassis = math.sqrt(self.nearest_point_to_chassis_x ** 2 + self.nearest_point_to_chassis_y ** 2)

      except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
          continue
      
      if self.nearest_point_to_chassis < 2 and self.nearest_point_to_chassis >= 1.65:
        level_msg = 2
        level_pub.publish(level_msg)
        # print ("Warning!! Must be slow!! Distance is %.2f." % self.nearest_point_to_chassis) 
        rospy.loginfo("Publish level 2.")
      elif self.nearest_point_to_chassis < 1.65:
        level_msg = 1
        level_pub.publish(level_msg)
        # print ("Dangerous!!! Must stop!!! Distance is %.2f." % self.nearest_point_to_chassis)
        rospy.loginfo("level 1.")
      else:
        level_msg = 3
        level_pub.publish(level_msg)
        # print ("No Dangerous. Distance is %.2f." % self.nearest_point_to_chassis) 
        rospy.loginfo("Publishing level 3.")

      time.sleep(0.1)
      
  def shutdownhook(self):
    self.ctrl_c = True

if __name__=='__main__':
  rospy.init_node('demonstrator_preprocessing')
  demonstrator_object=Demonstrator()

  try:
    demonstrator_object.read_laser()

  except rospy.ROSInterruptException:
    pass

