# Mechatronics II Romi Project
A MycroPython-based Romi robot porject use and STM32 board (via the 'pyb' module)

## Table of Contents
- [Overview & Objectives](#overview)
- [Features](#features)
- [Bill of Materials (BOM)](#bill-of-materials-bom)
- [Dependencies & Installation](#dependencies--installation)
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

- **Goal**: The primary goal of this project was to design, build, and program a robot, called Romi, capable of autonomously completing a predefined course using cooperative multitasking
- **Tasks**:
  - Detecting and following a black line while making the necessary route adjustments.
  - Navigating through a grid/tunnel section using heading information from a onboard IMU.
  - Detecting and responding to obstacles using bump sensors to detect collisions.
- **Solution**: We implemented a line sensor, bump sensor, and IMU heading information to navigate and complete the track.

**Track Reference**:
Below is a picture of the track used for the run:

```markdown
![Track Layout](docs/track_layout.jpg)
```
Romi can:
1. Follow black lines using IR sensors and a PID controller.  
2. Navigate a grid/tunnel utilizing IMU headings and encoder distance data.  
3. Detect collisions using bump sensors and respond accordingly.

**Demonstration**:
```markdown
![Romi Robot in Action](docs/romi_in_action.jpg)
[YouTube Demo Video](https://youtu.be/your-demo-link)
```


## Features
1. **Line-Following**: To keep the on track IR sensors and a PID controller were used.
2. **Grd/Tunnel Navigation**: To move in cardinal directions, encoders and IMU-based heading are used
3. 


In this project, a Pololu Romi chassis is outfitted with:
- An STM32-based microcontroller running MicroPython.
- A BNO055 IMU for orientation and heading data.
- Infrared sensors for line detection.
- Bump sensors for collision/wall detection.
- Two DC motors with encoders, driven by DRV8838 drivers, found in the power distribution board.
