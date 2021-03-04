# sicherheit_ws
Workshop for  security concept.

## Installation
1. Open a terminal and clone this repository.  
  
	`cd ~`  
  
	`git clone https://github.com/YunongPan/sicherheit_ws.git`  
  
2. Install submodules.  
  
	`cd ~/sicherheit_ws/src/sick_tim`  
  
	`git submodule update --init --recursive`  
  
3. Install dependencies.  
  
	`cd ~/sicherheit_ws`  
  
	`rosdep install --from-paths src --ignore-src -r -y`  
  
4. Build the workspace.  
  
	`catkin_make`  
  
## Using
1. Please start the project first and make sure the UR 10 robot is running.
  
	`roslaunch thesis_all start.launch`  
  
	`roslaunch flexarobos_perception mapping.launch`  
  
	`rosservice call /Mapping_server "save_location: ''"`  
  
2. Open another terminal and source the environment.
  
	`source ~/sicherheit_ws/devel/setup.bash`  
  
3. Make sure that both Lidar sensors are properly connected to the PC and start rosnodes for them.
  
	`roslaunch demonstrator_start_lidar demonstrator_start_lidar.launch`  
    
4. Open another terminal again and source the environment.
  
	`source ~/sicherheit_ws/devel/setup.bash`  
  
5. Start environment detection.
  
	`roslaunch demonstrator_preprocessing environmental_detection.launch`  
  
  	*Note: After starting this process, there will be a 10-second countdown. (It can be adjusted if you think it is too long/short. Please see section **Parameter**.)  Please use this time to be more than 2 meters away from the demonstrator. After the countdown is over, an environmental detection of about 10 seconds will be started. After this process is completely finished, you could return to the Demonstrator and continue to the next step.*  
  
	*If someone stays within 2 meters during the environmental detection, he/she may also be recognized as a stationary object and be filtered out, which may reduce the effectiveness of the program.*  
  	
6. Start speed control.
  
	`roslaunch laser_filters demonstrator_filter_total.launch`  
  
  	*Note: Please keep the surrounding environment unchanged, especially within 2 meters. If the environment has changed, (for example: the cabel of the interface is moved, or the table and chairs nearby are moved) please use* `ctrl + c` *to stop the process and repeat step 5 and step 6.*  
  
## Parameter
  
### The following parameters can be set in `environmental_detection.launch`.  
Path: `~/sicherheit_ws/src/demonstrator_preprocessing/launch/environmental_detection.launch`  
  
- **/countdown_seconds (default: 10 sec.)**
  - The time used to leave away from the demonstrator before starting the environment detection.
    
### The following parameters can be set in `demonstrator_filter_total.launch`
Path: `~/sicherheit_ws/src/laser_filters/launch/demonstrator_filter_total.launch`  
  
- **/demonstrator_speed_control/maximum_speed (default: 1.0 (100%))**
  - The speed of the robot when it is running without danger. Same as the robot speed displayed on the interface.
