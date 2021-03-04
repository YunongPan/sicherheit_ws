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
1. Please start the project first.
  
	`roslaunch thesis_all start.launch`  
  
	`roslaunch flexarobos_perception mapping.launch`  
  
	`rosservice call /Mapping_server "save_location: ''"`  
  
2. Open another terminal and source the environment.
  
	`source ~/sicherheit_ws/devel/setup.bash`  
  
3. Make sure that both Lidar sensors are properly connected to the PC and start rosnodes for them.
  
	`roslaunch demonstrator_start_lidar demonstrator_start_lidar.launch`  
    
4. Open another terminal again and source the environment.
  
	`source ~/sicherheit_ws/devel/setup.bash`  
  
5. Start environment detection..
  
	`roslaunch demonstrator_preprocessing environmental_detection.launch`  
  
  	*Before start the py.file please don't forget to set* `image_creator.py` *as an executable file:*  
  
	*Right click on* `image_creator.py` --> *Properties* --> *Permissions* --> *Allow executing file as program*
