#!/usr/bin/env python
import rospy
import roslib
roslib.load_manifest('demonstrator_preprocessing')
import time
import math
import tf
import geometry_msgs.msg
import message_filters
from sensor_msgs.msg import LaserScan




angle_min = -1.57079633
angle_max = 3.1415926536
sample = 811
angle_increment = (angle_max - angle_min) / sample  



### Main method
def main():
  rospy.init_node("environmental_detection_front")   
  box_id_total = []
  t = 0
  while t < 100:
    msg_origin = rospy.wait_for_message("/laserscan/front", LaserScan)
    print("Positions have been recorded.")

    global msg 
    msg = msg_origin
    msg.ranges = [float("inf") if x > 2.2 or x < 0.1 else x for x in msg_origin.ranges] ### The laser daten farther than 2.2 m will not be considered.
#  print msg.ranges



    position_x = list(range(len(msg.ranges)))
    position_y = list(range(len(msg.ranges)))

    for ind in range(len(msg.ranges)):

      point_angle = ind * angle_increment
      position_x[ind] = msg.ranges[ind] * math.cos(point_angle)
      position_y[ind] = msg.ranges[ind] * math.sin(point_angle + 0.0000001)  ## angle = 0, position_y = 0.0, may be wrong in the next step.

    filtered_position_x = [v for v in position_x if not math.isinf(v)]
    filtered_position_y = [v for v in position_y if not math.isinf(v)]
#  print filtered_position_x
#  print filtered_position_y

  
    box_num_x = list(range(len(filtered_position_x)))
    box_num_y = list(range(len(filtered_position_y)))
    box_id_x = list(range(len(filtered_position_x)))
    box_id_y = list(range(len(filtered_position_y)))
    box_id = list(range(len(filtered_position_x)))
    box_amount = 10
    box_side = 2.2 / box_amount
    for ind in range(len(filtered_position_x)):
      if filtered_position_x[ind] > 0:
        box_num_x[ind] = filtered_position_x[ind] // box_side + 1
        box_id_x[ind] = box_num_x[ind] + box_amount
      else:
        box_num_x[ind] = filtered_position_x[ind] // box_side
        box_id_x[ind] = box_num_x[ind] + box_amount + 1

      if filtered_position_y[ind] > 0:
        box_num_y[ind] = filtered_position_y[ind] // box_side + 1
        box_id_y[ind] = (box_num_y[ind] + box_amount) / 100
      else:
        box_num_y[ind] = filtered_position_y[ind] // box_side
        box_id_y[ind] = (box_num_y[ind] + box_amount + 1) / 100

      box_id[ind] = box_id_x[ind] + box_id_y[ind]
    box_id_total += box_id
    t += 1

#  print box_id_total
  box_id_filtered = []
  [box_id_filtered.append(i) for i in box_id_total if not i in box_id_filtered]
  box_id_filtered.sort()
  box_combi = ()
  box_combi_list = []

  i = 0

  box_combi_list.append(box_id_filtered[0]) 
  for k in range(1, len(box_id_filtered)): # leer/nur 1 element, wie?
    if int(box_id_filtered[k]) == int(box_id_filtered[k-1]):
      a = box_id_filtered[k] - int(box_id_filtered[k])
      b = box_id_filtered[k-1] - int(box_id_filtered[k-1]) + 0.01

      if a-b < 0.001:
        box_combi_list.append(box_id_filtered[k])

      else:
        box_combi_add = (box_combi_list,)
        box_combi += box_combi_add
        i += 1
        box_combi_list = []
        box_combi_list.append(box_id_filtered[k])
    else:

      box_combi_add = (box_combi_list,)
      box_combi += box_combi_add
      i += 1
      box_combi_list = []
      box_combi_list.append(box_id_filtered[k])

  box_combi_add = (box_combi_list,)
  box_combi += box_combi_add



#  print box_num_x
#  print box_num_y
#  print box_id
#  print box_id_filtered
#  print box_combi

  ScanFilterChain=list(range(len(box_combi)))
  for i in range(len(box_combi)):
    max_y = -(int(box_combi[i][0]) - box_amount - 1) * box_side + 0.45
    min_y = -(int(box_combi[i][0]) - box_amount) * box_side + 0.45
    min_x = ((box_combi[i][0] - int(box_combi[i][0])) * 100 - box_amount - 1) * box_side + 0.65
    max_x = ((box_combi[i][-1] - int(box_combi[i][0])) * 100 - box_amount) * box_side + 0.65
#    print min_x
#    print max_x
#    print min_y
#    print max_y
    min_z = -0.5
    max_z = 0.5
    ScanFilterChain[i] = {'type': 'laser_filters/LaserScanBoxFilter', 'params': {'min_x': min_x, 'min_y': min_y, 'min_z': min_z, 'invert': False, 'box_frame': 'chassis', 'max_z': max_z, 'max_x': max_x, 'max_y': max_y}, 'name': str(i)}

  rospy.set_param('/laser_box_filter_front/scan_filter_chain', ScanFilterChain)

  print("Parameters for front lidar have been updated.")
    

### Entry point
if __name__ == '__main__':
#  rospy.loginfo("Ten seconds countdown......")
#  print 0.0//0.22 +1
  print ("Ten seconds countdown......")
  for i in range(10):
    print (9 - i)
    time.sleep(1)
  main()

