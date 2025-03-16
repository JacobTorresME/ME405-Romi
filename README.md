# Mechatronics II Romi Project
A MycroPython-based Romi robot porject use and STM32 board (via the 'pyb' module)

## Table of Contents
- [Overview & Objectives](#overview--objectives)
- [Features](#features)
- [Bill of Materials (BOM)](#bill-of-materials-bom)
- [Electrical Design](#electrical-design)
- [Mechanical Design](#mechanical-design)
- [Motor Characterization](#motor-characterization)
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

## Electrical Design
The Romi is wirred to an STM32-L476RG Nucleo board. This allows for the integration of multiple sensors and motor controller that facilitate course navigation and obstacle detection. The set up includes:

- Power Source (6 double AA baterries)
- Power Distribution Board
- Encoders
- Bump Sensors
- Motor Drivers
- Line Sensor
- IMU (Inertial Measurement Unit)

A wiring diagram demonstrating how each one of the components above is connect can be seen in the diagrema below

**Wiring Diagram of Romi**
```markdown
Insert Romi wiring diagram here
```
This wiring diagram helped us ensure real-time feedback and control, which at the end was a crucial component that allowed Romi to navigate and complete the course. 

## Mechanical Design

Due to our team selecting that

## Motor Characterization
To properly control the DC motors we performed characterization tests for the left and right motors, to find the motors gain, time constant, and minimal effort required to make the motor turn. The tests consisted of producing a step response by setting the percent PWM going to each of the motors from 0% to 70%. We collected the Time, Position, and Velocity of each of the motors, at a sampling rate of 1000Hz, and saw how the properties of the motor evolved over time.

To find each motors gain and startup effort we extracted the steady-state velocity from the last data points of each run on the Velocity vs. Time plots. We then created a scatter plot of the Steady-State Velocity vs. Input Voltage and calculated the best fit line using linear regression. The slope of this line represented the motor gain and the y-intercept of the line represented the minimum voltage required to overcome static friction (startup effort). The Motor Gain and Startup Effort plots are shown below.

**Motor Gain and Minimum Effort Required Plot**
```mardown
Motor gain plot goes here
```
To calculate the each of the motors time constant (τ) we used a the following logarithmic transformation

$\ln \left( 1 - \frac{\omega}{\omega_{\max}} \right)$

where:

$$
\omega \text{ is the motor velocity at time } t
$$

$$
\omega_{\max} \text{ is the steady-state velocity}
$$

From here a linear regression was performed on the transformed data were the negative inverse of the slope was taken to determine each of the motors time constants (τ). The Linearized Output vs. Time plots are shown below. 

**Linearized Output vs. Time Plot**
```markdown
Plots go here
```

The resulting values determined in this step are shown below

| Motor | Motor Gain (rad/V*s) | Time Constant (s) | Minimum Effort Required (V) |
|-------|----------------------|-------------------|-----------------------------|
| Left  | 6.73                 | 0.0721            | 0.61                        |
| Right | 6.39                 | 0.0698            | 1.01                        |


## Code Descriptions

