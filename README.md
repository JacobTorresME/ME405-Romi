# Mechatronics II Romi Project
A MycroPython-based Romi robot porject use and STM32 board (via the 'pyb' module)

## Table of Contents
- [Overview & Objectives](#overview--objectives)
- [Features](#features)
- [Bill of Materials (BOM)](#bill-of-materials-bom)
- [Motor Characterization](#motor-characterization)
- [State-Space Model](#state-space-model)
- [Electrical Design](#electrical-design)
- [Mechanical Design](#mechanical-design)
- [Code Descriptions](#code-descriptions)
  - [Core Files](#core-files)
  - [Task Files](#task-files)

---

## Overview & Objectives

### Project Obejctive

**Goal**: The primary goal of this project was to design, build, and program a robot, called Romi, capable of autonomously completing a predefined course using cooperative multitasking

**Tasks**:
- Detecting and following a black line while making the necessary route adjustments.
- Navigating through a grid/tunnel section using heading information from a onboard IMU.
- Detecting and responding to obstacles using bump sensors to detect collisions.

**Solution**: We implemented a line sensor, bump sensor, and IMU heading information to navigate and complete the track.

**Track Reference**:

```markdown
![Track Layout](docs/track_layout.jpg)
```
**Romi can**:
  1. Follow black lines using IR sensors and a PID controller.  
  2. Navigate a grid/tunnel utilizing IMU headings and encoder distance data.  
  3. Detect collisions using bump sensors and respond accordingly.

**Romi Setup**:
The Romi has to be placed inside of the starting box facing the first line. The board remians plugged into the computer until the porgram has initialized successfully. Once initialization is complete, we unplugged Tomi from the computer, pressed the blue button on the Nucleo, and alllowed it to run on the course independently.

**Demonstration**:
```markdown
![Romi Robot in Action](docs/romi_in_action.jpg)
[YouTube Demo Video](https://youtu.be/your-demo-link)
```

## Features
1. **Line-Following**: Infrared sensor and a PID controller assist Romi in ramaining on track.
2. **Grid/Tunnel Navigation**: To move in cardinal directions, encoders and IMU-based heading were used.
3. **Collision Detection**: Bump sensors triggered by collision allow Romi to detect and maneuver obstacles encountered.
4. **MicroPython**: A STM32-based microcontroller runs python and leverages `cotask` and `task_share` for real-time task scheduling. Additionally, tasks are split into distinct `.py` modules to enable cooperative multitasking.
5. **Custom Mounts**: Custom 3D printed line sensor and bump senser mounts were implemented to allow for proper installation and usage.

## Bill of Materials (BOM)
| Item                | Quantity | Description                     | Link / Source       |
|---------------------|----------|---------------------------------|---------------------|
| Pololu Romi Chassis | 1        | Romi base with 2 DC motors      | [Pololu Romi](...)  |
| STM32-L476RG        | 1        | MicroPython-compatible MCU      | [STM32 Board](...)  |
| DRV8838 Drivers     | 1-2      | Motor drivers (if not onboard)  | [DRV8838](...)      |
| BNO055 Sensor       | 1        | IMU for orientation             | [BNO055](...)       |
| IR Sensors          | 13       | Reflective IR for line sensing  | [Sensors](...)      |
| Bump Switches       | 4        | Collision sensors               | [Switches](...)     |
| Assorted Wires      | Many     | Jumper cables, etc.            | —                   |

## Motor Characterization


## State-Space Model


## Electrical Design


## Mechanical Design


## Code Descriptions

