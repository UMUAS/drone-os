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

To get started with development of drone-os, please follow our [installation guide](https://github.com/UMUAS/drone-os/wiki/Installation).

<img width="1919" height="1031" alt="image" src="https://github.com/user-attachments/assets/ce74058a-3809-40cb-ac5c-ad301a3836a0" />

# Running on a drone
Deploying the software on the drone is supposed to be similar to the simulation and development stage. The main difference is that during deployment, the software needs to access the physical components instead of the simulated components. This will be achieved using common interfaces.

# Future Improvements
- Docker development environment
- Automated installation scripts
