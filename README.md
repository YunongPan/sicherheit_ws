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
  
## Testing
