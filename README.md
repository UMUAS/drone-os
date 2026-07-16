# Drone OS
Drone OS is the software stack used by the team to perform autonomous operations and that will perform tasks on the drone's companion computer (e.g. Raspberry Pi or Jetson).
It is a ROS2 workspace that contains packages required for simulation, autonomy, perception, mapping, communication, and mission execution.

This repository is designed to support multiple competition years while keeping the software architecture consistent. It goes along with [UMUAS/ground-station](https://github.com/UMUAS/ground-station) repository, which provides the ground crew with visualization, telemetry, and command execution.

# Features
Drone OS uses a modular software stack for autonomous UAVs to provide:
- Autonomous mission execution
- Object detection and tracking
- Obstacle avoidance
- Path planning
- Mapping and SLAM
- MAVLink/ArduPilot integration
- Simulation using ArduPilot SITL and Gazebo

# Repository Structure
```
drone-os/
|
|- config/             # Shared configuration
|- scripts/            # Utility scripts
|
|- src/
|  |- drone_bringup/   # ROS2 launch files
|  |- interfaces/      # Custom ROS2 messages and services
|  |- mission/         # Mission execution and decision making
|  |- planning/        # Path planning and obstacle avoidance
|  |- perception/      # Vision and object detection
|  |- mapping/         # SLAM and 2D/3D mapping
|  |- simulation/      # Simulation-specific content such as launch files, Gazebo worlds, models, etc.
```

# Development Workflow
The recommended workflow is:

1. Develop and test packages locally.
2. Validate behaviour in simulation using ArduPilot SITL and Gazebo.
3. Test integration with the complete Drone OS launch.
4. Deploy to the companion computer.
5. Perform real-world flight testing.

Simulation should always be completed before hardware testing.


# Getting Started
Developing the software does not require physical hardware. ArduPilot SITL and Gazebo can be used to simulate drone behaviour, which can reduce risks when flying on the drone. 

## Requirements
- Ubuntu 24.04 LTS
- ROS2 Jazzy

If you want to run Ubuntu 24.04 LTS on your computer, there are a few options:
- Windows users:
  - (recommended) WSL
  - Virtual Machine (e.g. VirtualBox)
  - (advanced) Dual boot Ubuntu alongside Windows
  - Docker
- MacOS users:
  - Virtual Machine (e.g. VirtualBox)
  - Docker

> [!NOTE]
> If you decide to use Docker, you will need to perform the installation process yourself and compose your own Docker images. However, support for Docker is being considered because Docker provides the simplest installation process and best consistency across different machines.
> 
> We also plan to provide an automated installation script in the future to simplify the setup process for non-Docker installations.

## Installing ROS2 Jazzy
Once you installed Ubuntu 24.04 LTS, we will now install ROS2 Jazzy. Jazzy is not the latest version, but is still newer version than ROS2 Humble which is used in the ArduPilot tutorial. 

First, you will need to follow the instructions on how to install ROS2: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
> [!IMPORTANT]
> When given the option, you should choose to run ```sudo apt install ros-jazzy-desktop``` instead of ```sudo apt install ros-jazzy-ros-base```.

By now, every time you want to access ROS2 commands in the terminal, you first need to source the setup file. This can be automated by running the following in your terminal:
```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
([source](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html#add-sourcing-to-your-shell-startup-script))

## Preparing ROS2 for ArduPilot
Since we are using ROS2 Jazzy instead of ROS2 Humble, the official ArduPilot [installation guide](https://ardupilot.org/dev/docs/ros2-install.html) will be slightly different. The modified step-by-step instructions are provided below. For more information on each step, especially if troubleshooting is needed, please refer to the official guide.

```bash
mkdir -p ~/ardu_ws/src
cd ~/ardu_ws/src
git clone --recurse-submodules -b master https://github.com/ArduPilot/ardupilot.git
git clone --recurse-submodules -b jazzy https://github.com/micro-ROS/micro-ROS-Agent.git
```

Now update all dependencies for _micro-ROS-Agent_:
```bash
cd ~/ardu_ws
sudo apt update
sudo rosdep init
rosdep update
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
```

Installing the _Micro-XRCE-DDS-Gen_ build dependency:
```bash
sudo apt install default-jre
cd ~/ardu_ws
git clone --recurse-submodules --branch v4.7.0 https://github.com/ardupilot/Micro-XRCE-DDS-Gen.git
cd Micro-XRCE-DDS-Gen
./gradlew assemble
```

> [!TIP]
> If `./gradlew assemble` gives issues, some possible causes are:
> 
> The current Java version is too new for _Gradle 7.6_, which should be Java17. To fix:
> ```bash
> sudo apt install openjdk-17-jdk java-common
> sudo update-alrternatives --config java
> ```
> Select the option with **java 17**. Lastly, run:
> ```bash
> cd ~/ardu_ws/Micro-XRCE-DDS-Gen
> export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
> ./gradlew assemble
> ```
> 
> You might also be missing pexpect. To fix: 
> `python3 -m pip install --user pexpect` or `sudo apt install python3-pexpect`

Now, add the _Micro-XRCE-DDS-Gen_ scripts to ~/.bashrc:
```bash
echo "export PATH=\$PATH:$PWD/scripts" >> ~/.bashrc
source ~/.bashrc
```

Test _Micro-XRCE-DDS-Gen_ installation:
```bash
microxrceddsgen -help
# This should print out a help message
```

And finally, build your workspace:
```bash
cd ~/ardu_ws
colcon build --packages-up-to ardupilot_dds_tests
```

To test your installation, run:
```bash
cd ~/ardu_ws
source ./install/setup.bash
colcon test --executor sequential --parallel-workers 0 --base-paths src/ardupilot --event-handlers=console_cohesion+
colcon test-result --all --verbose
```

This concludes the first part of the installation. You will now need to build ArduPilot SITL.

## Installing ArduPilot SITL
Again, we modified the official instructions to let it function with ROS2 Jazzy. Official guide: https://ardupilot.org/dev/docs/ros2-sitl.html

```bash
cd ~/ardu_ws/src/ardupilot
./Tools/environment_install/install-prereqs-ubuntu.sh -y
```

```bash
cd ~/ardu_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-up-to ardupilot_sitl
source ~/.profile
```

You can now launch the SITL in ROS2 with the following commands:
```bash
cd ~/ardu_ws/
source install/setup.bash
ros2 launch ardupilot_sitl sitl_dds_udp.launch.py \
transport:=udp4 \
synthetic_clock:=True \
wipe:=False \
model:=quad \
speedup:=1 \
slave:=0 \
instance:=0 \
defaults:=$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/copter.parm,$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/dds_udp.parm \
sim_address:=127.0.0.1 \
master:=tcp:127.0.0.1:5760 \
sitl:=127.0.0.1:5501
```

Ensure the ArduPilot ROS nodes appear by running the following on a **seperate terminal**:
```bash
source ~/ardu_ws/install/setup.bash
# See the node appear in the ROS graph
ros2 node list
# See which topics are exposed by the node
ros2 node info /ap
# Echo a topic published from ArduPilot
ros2 topic echo /ap/geopose/filtered
```

To test and fly around, you can launch a MAVProxy instance in yet another terminal:

```bash
mavproxy.py --console --map --aircraft test --master=:14550
```

The final step is to install Gazebo.

## Installing Gazebo
The official ArduPilot guide for ROS2+Gazebo uses Gazebo Harmonic version, which works with ROS2 Jazzy. Again, be sure to install required dependencies for ROS2 Jazzy, not ROS2 Humble.
https://ardupilot.org/dev/docs/ros2-gazebo.html

Install standalone Gazebo:
```bash
sudo apt-get update
sudo apt-get install curl lsb-release gnupg

sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
```

Installation of Gazebo for ROS2:
```bash
sudo apt-get install ros-jazzy-ros-gz
```

Clone required repositories:
```bash
cd ~/ardu_ws/src
git clone --recurse-submodules -b ros2 https://github.com/ArduPilot/ardupilot_gazebo.git
git clone --recurse-submodules -b main https://github.com/ArduPilot/ardupilot_gz.git
git clone --recurse-submodules -b main https://github.com/ArduPilot/SITL_Models.git
mv SITL_Models ardupilot_sitl_models

git clone --recurse-submodules -b jazzy https://github.com/gazebosim/ros_gz.git
git clone --recurse-submodules -b jazzy https://github.com/ros/sdformat_urdf.git
```

Run to add in ~/.bashrc
```bash
echo "export GZ_VERSION=harmonic" >> ~/.bashrc

source ~/.bashrc
```

Update ROS and Gazebo dependencies:
```bash
cd ~/ardu_ws
source /opt/ros/jazzy/setup.bash
sudo apt update

sudo bash -c 'wget https://raw.githubusercontent.com/osrf/osrf-rosdep/master/gz/00-gazebo.list -O /etc/ros/rosdep/sources.list.d/00-gazebo.list'
rosdep update
rosdep resolve gz-harmonic
rosdep install --from-paths src --ignore-src -y
```

Build:
```bash
cd ~/ardu_ws
colcon build --packages-up-to ardupilot_gz_bringup
```

Test:
```bash
cd ~/ardu_ws
source install/setup.bash
colcon test --packages-select ardupilot_sitl ardupilot_dds_tests ardupilot_gazebo ardupilot_gz_applications ardupilot_gz_description ardupilot_gz_gazebo ardupilot_gz_bringup
colcon test-result --all --verbose
```

Run:
```bash
source install/setup.bash
ros2 launch ardupilot_gz_bringup iris_runway.launch.py
```

If launching iris_runway does not show a drone inside Gazebo and RViz, it probably is because it coudln't access the drone model. To do so, run:
```bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/ardu_ws/install/ardupilot_gazebo/share
```
For some reason, `echo $GZ_SIM_RESOURCE_PATH` only includes the worlds/ and models/ directories that are inside the share/ directory. This step fixed that temporarily. You can also add it into `~/.bashrc` to make the change permanent. This might be an ArduPilot mistake generated during the "colcon build".

<img width="1919" height="1031" alt="image" src="https://github.com/user-attachments/assets/ce74058a-3809-40cb-ac5c-ad301a3836a0" />


# Running on a drone
Deploying the software on the drone is supposed to be similar to the simulation and development stage. The main difference is that during deployment, the software needs to access the physical components instead of the simulated components. This will be achieved using common interfaces.

# Future Improvements
- Docker development environment
- Automated installation scripts 
