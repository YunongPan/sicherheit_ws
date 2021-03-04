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
  
  	*Note: After starting this process, there will be a 10-second countdown. Please use this time to stay away from the Demonstrator to 2 meters away. After the countdown is over, an environmental detection of about 10 seconds will be started. After this process is completely finished, you can go back to the Demonstrator and contine to the next step.*  
  
	*If someone stays within 2 meters during the environmental detection, he/she may also be recognized as a stationary object and be filtered out, which may reduce the effectiveness of the program.*  
  
	*Right click on* `image_creator.py` --> *Properties* --> *Permissions* --> *Allow executing file as program*
