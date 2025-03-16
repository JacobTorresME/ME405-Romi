# Mechatronics Romi Project
A MycroPython-based Romi robot porject use and STM32 board (via the 'pyb' module)

## Table of Contents
- [Overview & Objectives](#overview--objectives)
- [Features](#features)
- [Bill of Materials (BOM)](#bill-of-materials-bom)
- [Electrical Design](#electrical-design)
- [Mechanical Design](#mechanical-design)
- [Motor Characterization](#motor-characterization)
- [Code Description](#code-descriptions)

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

The mechanical design modifications to the original Romi chasis were primarily driven by the need to accomodate our long 14mm x 13 line sensor at the front of Romi. This key adjustment lead to one more smaller modification to the bump sensors. All the necessary CAD files for these modifications can be found in the CAD folder at the top of the repository. 

### Line Sensor Mount
Due to our line sensor being 14 mm in length the conventional standoff configuration rendered impractical without additional modifications. To securely mount our line sensor, we 3D printed custom bracket arms, as shown below. These bracket arms allowed us to use the original standoffs and position the line sensor flush with the bottom of Romis chassis and at the very front of Romi for optimal performance. 

**CAD picture of Line-Sensor Arms**
```mardown
CAD picture of the Mounts
```

### Bump Sensor Mounts
In adjusting our Romi chassis to accommodate thr line sensor, we inadvertently caused some fitment issues with the bump sensors. The bolts securing the standoffs prevented the bump sensors from sitting flush on top of Romi. Additionally, the bump sensors did not extend far enough past the line sensor, leaving it exposed and failing to detect collisions in these places. To resolve this, we fabricated two custom brackets: an L-shaped bracket and a straight bracket for each of the bump sensors. These brackets allowed the sensors to be mounted securely while ensuring they extended far enough to protect the line sensor and detect obstacles effectively. Furthermore, each bracket was __mm thick, allowing a precise fit above the bolts securing components at the bottom of the Romi chassis. Finally, the combination of both brackets allowed for the bump sensors to remain rigid and in place, including after collision. 

**CAD Picture of Bump Bracket Arms**
```mardown
CAD picture of the Mounts
```

### Romi Assembly
The bracket arms for the line sensors were secured using M2.5 bolts while the bracket arms for the bump sensors were secured using M2.0 bolts. Additionally, the bump sensors used washers and M2.0 nuts to fully secure the bump sensors onto the Romi chassis. The fully assembled Romi can be seen in the picture below. 



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

### Scheduler

#### **main.py**

**Purpose**:
`main.py` is the central coordinating file that initializes shared data structures and creates task objects. In addition, it uses cooperative multitasking through the use of `cotask` to "hop" between tasks. Most importantly, this is were you set up each individual task and manage which tasks run, in what order, and how frequentely. 

**Inner Workings**:
1. **Share Initialization**
   - At the top of `main.py`, there is multiple lines of code that create shared variables using `task_share.Share()`.
   - Examples are shown below:
   ```python
   yaw_rate       = task_share.Share('f', thread_protect=False, name="yaw_rate")
   omega_r        = task_share.Share('f', thread_protect=False, name="omega_r")
   run_flg        = task_share.Share('i', thread_protect=False, name="run_flg")
   ...
   ```

   Each of these labels is a global data structute for inter-task communication. An example of this is, `yaw_rate` is a float that tasks can write to (e.g., line-following logic) and read from (e.g., motor tasks)

2. **Task Creation**
   - `main.py` also instantiates each task object from the corresponding task file
   - This file gives each task object 3 things:
     - A priority (the order in which the schedular checks the task)
     - A period (How oftern they should run, in milliseconds)
     - A list of shared variables that they need to read from or write to.
   - For example:
     ```python
     task2 = cotask.Task(task2_right_motor.generator, name="Task_2",
                        priority=4, period=10, profile=True, trace=False, 
                        shares=(omega_r, run_flg))
     ```
3. **Schedular Setup**
   - After creating tasks, `main.py` appends each one to `cotask.task_list` and then calls `cotask.task_list.pri_sched()`. This runs a infinite loop that continously calls each task's generator function in order of priority, handling and executing multiple tasks at the same time behind the scenes.

4. **Exception Handling and Cleanup**
   - The file wraps the scheduling call in a `try-except` block to catch runtime erros and `KeyboardInterrupt` that stops the program. When a error occurs, it disables the motors and prints a message exiting safely. 

**Table of Shared Variables**
| Variable           | Type   | Description |
|--------------------|--------|-------------|
| `yaw_rate`        | *float* | Desired yaw rate (turning speed) for steering. |
| `omega_r` / `omega_l` | *float* | Angular velocity commands for the right and left motors, respectively. |
| `run_flg`         | *int*   | Flag indicating whether the motors should be running (`1`) or stopped (`0`). |
| `grid_flg`        | *int*   | Signals the robot to enter or exit grid/tunnel navigation logic. |
| `fwd_flg`         | *int*   | Controls movement: **1 = Forward**, **2 = Backward**, **0 = Idle**. |
| `line_follow_flg` | *int*   | Enables (`1`) or disables (`0`) line-following logic. |
| `line_flg`        | *int*   | Indicates whether a line was **lost (1)** or **found (0)** (used by Master Mind for transitions). |
| `line_value`      | *int*   | Numeric data about line detection (**0 = On-line**, **1 = Off-line**). |
| `bump_flg`        | *int*   | Collision detection flag, set to **`1`** when a bumper switch is triggered. |

These shares are a key component that enables tasks to communicate in a cooperative manner.

### Tasks

Each one of these tasks use a **Finite State Machine** within each of their `generator()` functions. Each tasks `generator()` function starts typically with a `S0_STANBY`, `S1_RUN`, etc., and transitions occur based on flags or sensor readings.  

#### **1. MM.py (Master Mind)**

- **Purpose**: Acts as the main handler, it implements a FSM machine to control overall behavior
- **FSM State Breakdown**
1. `S0_STANDBY`:
    - Waits for a user button press or for the `run_flg` to become `
    - One triggered, it moves to finding the.
2. `S1_FIND_LINE`:
    - Tells the motors to drive straight until the Infrared sensors detect a line.
    - Once a line is found it sets `line_follow_flg = 1` and transitions.
3. `S2_LEVEL_1` (Line Follow Mode)
    - Starts the line-following action. Monitors `line_flg` to see if it has lost the line or detects an intersection, moves to next state.
    - If a the `bump_flg = 1` (collision occurs, it transitions to a collision handling state.
4. `S3_GRID_LEVEL`
    - Sets `grid_flg = 1` and allows **grid_task.py** to take over. This may occur when the robot has traveled a certain distance or reached a marker.
    - Exits the state once the grid/tunnel section is done. 
5. `S4_EXIT_TUNNEL`
    - Handles the logic when leaving the tunnel or grid area. It check the `line_value` variable to find a line.
6. `S5_HITTING_WALL`
    - A state that keeps driving forward until the bump sensors are triggered.  
    - When the collision occurs, sets `bump_flg = 1`; transitions to next state.
7. `S6_MOV_BACK`  
     - Moves backward a certain distance (setting `fwd_flg = 2`).  
     - When done, transitions to the next state.
8. `S7_TURN_NORTH`  
     - Uses IMU heading to rotate Romi back north.  
     - When the heading is aligned, transitions to next state.
9. `S8_DRIVE_NORTH`  
     - Drives Romi north and uses encoders to measure distance.  
     - Moves to the next state upon reaching a certain distance.
10. `S9_TURN_WEST`  
      - Another heading-based rotation points Romi west.  
      - Waits until heading is correct, then transitions to next state.
11. `S10_DRIVE_WEST`  
      - Drives west for a set distance using the encoders to measure distance traveled.  
      - Moves to the next state upon reaching a certain distance.
12. `S11_TURN_SOUTH` / `S12_DRIVE_SOUTH`  
      - These states align the robot south and drive it, eventually returning to the starting point.

- **Key Variables**  
  - `run_flg` to see if it should run or not.  
  - `bump_flg` for collisions.  
  - `line_flg` / `grid_flg` to move between line follow and grid tasks.  
  - `fwd_flg` sets forward or backward motion.
  - `yaw_rate` or `omega_r/l` for controlling turning or speed in each state.

- **How it Works**
  - Each Finite State Machine state in the generator function checks relevant flags/sensors.  
  - If conditions are met it transitions to the next state.
  - This set up allows Master Mind to set a step by step process for Romi from initial placement all the way back to the start.

  

#### **2. grid_task.py**

- **Purpose**: This task is in charge of the grid/tunnel navigation portion, using an internal FSM to perform heading adjustments and distance-based travel.
- **FSM State Breakdown**
1. `S0_INIT`  
     - Reads and stores the robot’s current IMU heading.  
     - Waits for `grid_flg == 1`.
2. `S1_STANDBY`  
     - Idle state, monitoring `grid_flg`.
     - If `grid_flg` becomes 1 it proceeds to the next state.
3. `S2_TURN_SOUTH`  
     - Alings Romis heading to 2880, representing south.  
     - Continuously reads the heading from the IMU
     - Updates `yaw_rate` using a small heading PID (or direct turn logic).  
     - Once aligned, sets `fwd_flg = 1`and transitions to the next state.
4. `S3_DRIVE_SOUTH`  
     - Moves forward until encoders indicate a certain distance.  
     - Once the distance is reached it transitions to the next state.  
     - Once the tunnel ends it sets `grid_flg = 0` to exit grid mode.
  
- **Key Variables**  
  - `heading` from `IMU.py`.  
  - `left_start` / `right_start` for storing initial encoder positions.  
  - `grid_flg` to activate or deactivate the grid task.  
  - `yaw_rate` sets turning commands.

- **How It Works**  
  - Each time the generator runs, it checks its current FSM state.  
  - Aligns Romis heading and drives a fixed distance in that prescribed heading.  
  - Moves to the next state when the target heading or distance is achieved.
 
#### **3. line_task.py**

- **Purpose**: This task is in charge of performing line-following using a Infrared sensor data and a PID for steering correction.
- **FSM State Breakdown**  
1. `S0_STANDBY`
   - Waits for `line_follow_flg == 1`.
2. `S1_RUN`:
   - Actively calculates line offset, feeding a PID to adjust `yaw_rate`.
- **Key Variables**  
  - `line_follow_flg`, `fwd_flg`, `yaw_rate`.  
  - Reads the Infrared sensor centroid from `IR_Array.py`.
- **How It Works**  
  - In the `SO_STANDBY` state it waits to be activated 
  - While it is in `S1_RUN` state, during each cycle run it...
     - Gets the IR centroid.  
     - Error of the centriod (centroid - 7).  
     - Uses a PID to calculate a correction.  
     - The correction is written to `yaw_rate`, which **motorstask.py** uses for left/right speed differences.

#### **4. line_finder.py**

- **Purpose**: The task is in charge of alerting the system when the line is lost or re-found.
- **FSM State Breakdown**
1. `S0_LOOK_FOR_LINE`
    - If IR data indicates a line is lost, sets `line_flg = 1`, transitions to `S1_LOOK_FOR_ACK`.  
2. `S1_LOOK_FOR_ACK`  
    - Waits until `line_flg` is cleared. Then returns to `S0_LOOK_FOR_LINE`.
- **Key Variables**  
  - `line_flg`, `line_value`.  
- **How It Works**  
  - Summation or threshold logic checks IR readings.  
  - If it crosses a threshold, notifies the rest of the system via `line_flg`.  
  - Master Mind or line_task acknowledges by resetting `line_flg`.
