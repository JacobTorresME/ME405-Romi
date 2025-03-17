# Mechatronics Romi Project
A MycroPython-based Romi robot project using an STM32 board (via the 'pyb' module). 

**By Jacob Torres and Carter Josef**

## Table of Contents
- [Overview & Objectives](#overview--objectives)
- [Features](#features)
- [Bill of Materials (BOM)](#bill-of-materials-bom)
- [Electrical Design](#electrical-design)
- [Mechanical Design](#mechanical-design)
- [Motor Characterization](#motor-characterization)
- [Code Description](#code-descriptions)
  1. [Scheduler](#scheduler)
  2. [Tasks](#tasks)
  3. [Driver Classes](#driver-classes)
- [Finite State Machines](#finite-state-machines)
 

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

![Track](https://github.com/user-attachments/assets/4f613982-a758-495c-ba7b-723a83e253e3)

**Romi can**:
  1. Follow black lines using IR sensors and a PID controller.  
  2. Navigate a grid/tunnel utilizing IMU headings and encoder distance data.  
  3. Detect collisions using bump sensors and respond accordingly.

**Romi Setup**:
The Romi has to be placed inside of the starting box facing the first line. The board remians plugged into the computer until the porgram has initialized successfully. Once initialization is complete, we unplugged Tomi from the computer, pressed the blue button on the Nucleo, and alllowed it to run on the course independently.

**Romi**:

![Romi](https://github.com/user-attachments/assets/e1513827-d615-40be-9a17-84f75ae3b03e)

**Demonstration**:

[YouTube Demo Video](https://www.youtube.com/watch?v=X8mRvTR4OUs)

## Features
1. **Line-Following**: Infrared sensor and a PID controller assist Romi in ramaining on track.
2. **Grid/Tunnel Navigation**: To move in cardinal directions, encoders and IMU-based heading were used.
3. **Collision Detection**: Bump sensors triggered by collision allow Romi to detect and maneuver obstacles encountered.
4. **MicroPython**: A STM32-based microcontroller runs python and leverages `cotask` and `task_share` for real-time task scheduling. Additionally, tasks are split into distinct `.py` modules to enable cooperative multitasking.
5. **Custom Mounts**: Custom 3D printed line sensor and bump senser mounts were implemented to allow for proper installation and usage.

## Bill of Materials (BOM)
| Item                | Quantity | Description                     | Link / Source       |
|---------------------|----------|---------------------------------|---------------------|
| Pololu Romi Chassis | 1        | Romi base with 2 DC motors      | [Pololu Romi](https://www.pololu.com/category/203/romi-chassis-kits)  |
| STM32-L476RG        | 1        | MicroPython-compatible MCU      | [STM32 Board](https://estore.st.com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-nucleo-boards/nucleo-l476rg.html)  |
| Power Distribution Board & DRV8838 Motor Drivers     | 1         | Distributes power and contains two motor drivers  | [Power Distribution Board](https://www.pololu.com/product/3543)      |
| BNO055 Sensor       | 1        | IMU for orientation             | [BNO055](https://www.adafruit.com/product/2472)       |
| IR Sensors          | 1       | Reflective IR for line sensing  | [IR Sensors](https://www.pololu.com/category/203/romi-chassis-kits)      |
| Bump Switches       | 2        | Collision sensors               | [Left Bump Sensor](https://www.pololu.com/product/3673) [Right Bump Sensor](https://www.pololu.com/product/3674) |
| Dupont Wires      | Many     | Female to female            | [Wires](https://www.amazon.com/dp/B07GCY6CH7?th=1)                   |

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

![Wirring diagram](https://github.com/user-attachments/assets/00a5ec8c-57e4-498f-9205-3ae597e32f00)

This wiring diagram helped us ensure real-time feedback and control, which at the end was a crucial component that allowed Romi to navigate and complete the course. 

## Mechanical Design

The mechanical design modifications to the original Romi chasis were primarily driven by the need to accomodate our long 14mm x 13 line sensor at the front of Romi. This key adjustment lead to one more smaller modification to the bump sensors. All the necessary CAD files for these modifications can be found in the CAD folder at the top of the repository. 

### Line Sensor Mount
Due to our line sensor being 14 mm in length the conventional standoff configuration rendered impractical without additional modifications. To securely mount our line sensor, we 3D printed custom bracket arms, as shown below. These bracket arms allowed us to use the original standoffs and position the line sensor flush with the bottom of Romis chassis and at the very front of Romi for optimal performance. 

**CAD picture of Line-Sensor Arms**

![IRsensor](https://github.com/user-attachments/assets/7b22426c-50b5-4191-b391-41907beb0665)


### Bump Sensor Mounts
In adjusting our Romi chassis to accommodate thr line sensor, we inadvertently caused some fitment issues with the bump sensors. The bolts securing the standoffs prevented the bump sensors from sitting flush on top of Romi. Additionally, the bump sensors did not extend far enough past the line sensor, leaving it exposed and failing to detect collisions in these places. To resolve this, we fabricated two custom brackets: an L-shaped bracket and a straight bracket for each of the bump sensors. These brackets allowed the sensors to be mounted securely while ensuring they extended far enough to protect the line sensor and detect obstacles effectively. Furthermore, each bracket was __mm thick, allowing a precise fit above the bolts securing components at the bottom of the Romi chassis. Finally, the combination of both brackets allowed for the bump sensors to remain rigid and in place, including after collision. 

**CAD Picture of Bump Bracket Arms**

![Lbrackets](https://github.com/user-attachments/assets/0cbf78c7-c276-42ef-b838-8ac41f9c919c)
![straightbracket](https://github.com/user-attachments/assets/5bcad4c5-5f56-4dc2-9b05-b571167e1617)

### Romi Assembly
The bracket arms for the line sensors were secured using M2.5 bolts while the bracket arms for the bump sensors were secured using M2.0 bolts. Additionally, the bump sensors used washers and M2.0 nuts to fully secure the bump sensors onto the Romi chassis. 

## Motor Characterization
To properly control the DC motors we performed characterization tests for the left and right motors, to find the motors gain, time constant, and minimal effort required to make the motor turn. The tests consisted of producing a step response by setting the percent PWM going to each of the motors from 0% to 70%. We collected the Time, Position, and Velocity of each of the motors, at a sampling rate of 1000Hz, and saw how the properties of the motor evolved over time.

To find each motors gain and startup effort we extracted the steady-state velocity from the last data points of each run on the Velocity vs. Time plots. We then created a scatter plot of the Steady-State Velocity vs. Input Voltage and calculated the best fit line using linear regression. The slope of this line represented the motor gain and the y-intercept of the line represented the minimum voltage required to overcome static friction (startup effort). The Motor Gain and Startup Effort plots are shown below.

**Motor Gain and Minimum Effort Required Plot**

![Motor Gain Right](https://github.com/user-attachments/assets/bfdc0774-277a-4a3b-8fa5-8c5f93a92a9d)

![Motor Gain Left](https://github.com/user-attachments/assets/c656dc40-7df3-4b04-820e-04f81bc7017b)

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

![Linerized Right](https://github.com/user-attachments/assets/df6875b3-0d9c-4665-aa6e-a6213b968579)

![Linerized Left](https://github.com/user-attachments/assets/df80ad48-20e9-4971-9707-cb51dc96db5a)

The resulting values determined in this step are shown below

| Motor | Motor Gain (rad/V*s) | Time Constant (s) | Minimum Effort Required (V) |
|-------|----------------------|-------------------|-----------------------------|
| Left  | 6.73                 | 0.0721            | 0.61                        |
| Right | 6.39                 | 0.0698            | 1.01                        |

## Block Diagram of the System

The following diagram is a visual representation of the control diagram used for Romi. We opted for the cascaded control system. We used a PID controller for each wheel. The input to this is a motor speed. The encoder provides feedback to ensure that each wheel is spinning at the desired rate. Linear velocity and angular velocity of Romi are decoupled into individual wheel velocities. This is checked with a PID controller using the IMU and line sensor for feedback.

![System block diagram](https://github.com/user-attachments/assets/61e7de7e-2b91-491c-856e-ba027a907a41)

## Task Diagram

The following diagram is a visual representation of the different tasks within our program. Each task is discussed in further detail below.

![Task Diagram](https://github.com/user-attachments/assets/bc643e5d-b804-4495-b54b-274ff1b2d720)

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

---

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
5. `S4_TURN_WEST`
     - A final aligment step. Waits until heading is 4320, correspoding to West.
     - Sets `fwd_flg = 1` before returning to standby state.
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
    - If the data received from the IR indicates is no line it sets `line_flg = 1` and transitions to the next state.
2. `S1_LOOK_FOR_ACK`  
    - Waits until `line_flg` is cleared, once it is cleared it returns to `S0_LOOK_FOR_LINE`.
- **Key Variables**  
  - `line_flg`, `line_value`.  
- **How It Works**  
  - A set threshhold checks IR readings.  
  - If it crosses this threshold it notifies the rest of the system using the `line_flg` share.  
  - Master Mind or line_task acknowledges by resetting `line_flg`.
 
#### **5. motorstask.py**

- **Purpose**: This task performs closed-loop motor control for left and right wheels. It performs this by reading the encoders and applying PID or a feedfoward gain.
- **FSM**  
1. `S0_STANDBY`
   - Motors remain desabled if `run_flag == 0`
   - If `run_flag == 1` it transitions to the next state   
2. `S1_RUN`
   - Once `run_flg == 1` it reads `omega_r` / `omega_l` from shares
   - It then uses a PID to match actual speeds.
- **Key Variables**  
  - `omega_r`, `omega_l`, `run_flg`.  
  - Encoder velocity feedback from `Encoder.py`.
- **How It Works**  
  - If `run_flg` = 1, calls `Motor.enable()`, enabling the motors.  
  - Compares actual speed to the setpoint.  
  - Uses `PID.py` to calculate an effort and then calls `Motor.set_effort(effort)` to physically drive the motor to the setpoint.
 
#### **6. Collision_Detect_task.py**

- **Purpose**: The purpose of this task it to monitor the bumper states and detect collisions. If a collision occurs it raises a flag for Master Mind to handle.
- **FSM**  
1. `S0_WAIT_FOR_COLLISION`  
    - If a bumper press is detected (`task_Bump.py`), sets `bump_flg = 1`.
    - If `bump_flg = 1` it transitions to the next state.
2. `S1_ACKNOWLEDGE_COLLISION`  
    - Waits until `bump_flg` is cleared by **MM.py**.
    - One `bump_flg` is cleared it then returns to `S0_WAIT_FOR_COLLISION`.
- **Key Variables**  
  - `bump_flg`: collision flag.  
- **How It Works**  
  - During each cycle run it checks if any bumper has been pressed.  
  - If collision occurs and the bumper is pressed it sets `bump_flg = 1` so that Master Mind or other logic can respond.

---

### Driver Classes

#### 1. Encoder.py
- **Purpose**: This class is in charge of interpreting quadrature encoder signals and producing both position and velocity data for each motor.
- **What It Does**:
  - Configures a timer in ENC_AB mode for pins (chA, chB).
  - The `update()` method calculates `delta`, which is equal to, current counter - `prev_count`.
  - Corrects for overflow if the timer wraps.
  - Accumulates `position` and calculates velocity by storing deltas over time.
  - Returns linear positon in mm using wheel geometry through the `get_lin_position` method.
- **Assigned to Help**:
  - **motorstask.py**: uses encoder velocity for PID speed control.
  - **grid_task.py**: uses position to measure distance traveled during tunnel navigation.

#### 2. Motor.py
- **Purpose**: This class offers an interface for controlling a DC motor’s direction and speed though PWM signals.
- **What It Does**:
  - Sets up a timer channel for PWM output, direction pin, and a sleep pin.
  - In the `set_effort(effort)` method it uses the sign of `effort` to set direction and the magnitude for the PWM duty cycle.
- **Assigned to Help**:
  - **motorstask.py**: uses `set_effort()` each cycle to realize the PID output for each motor.
  - **MM.py**: and other tasks can call `enable()` / `disable()` to stop Romi safely.

#### 3. IMU.py
- **Purpose**: This class communicates with the BNO055 IMU sensor to obtain heading, roll, pitch, and calibration data.
- **What It Does**:
  - Uses I²C to configure the BNO055 in a particular mode (e.g., IMU, NDOF).
  - The `read_eul_angles()` method retrieves heading, roll, and pitch Euler angles from internal registers.
  - Provides read/write functions for calibration or operation modes.
- **Assigned to Help**:
  - **grid_task.py**: uses this class for cardinal direction turning.
  - **MM.py**: uses this class for cardinal directions to help with transitions

#### 4. IR_Array.py
- **Purpose**: This class combines multiple IR sensors into one array, providing a centroid.
- **What It Does**:
  - Instantiates multiple `IR_Sensor.py` objects, each referencing a different ADC pin.
  - The `update()` method iterates through each sensor, collects normalized values, computes unweighted (`u_sum`) and weighted (`w_sum`) sums.
  - The `get_centroid()` method returns a float in the 0 to 13 range, indicating line offset.
  - The `find_line()` method returns an integer code, were 0 = on a line, 1 = line lost, 2 = thick line.
- **Assigned to Help**:
  - **line_task.py**: uses this class for continuous line following.
  - **line_finder.py**: uses this class for transitions or intersection detection.

#### 5. IR_Sensor.py
- **Purpose**: This class is a low-level driver class used for a single IR sensor, reading ADC and normalizing it based on black/white calibration.
- **What It Does**:
  - Defines `self.white` and `self.black` thresholds found through `sensor_calibration.py`.
  - The `update()` method reads raw ADC values and then transforms it into a 0–1000 scale.
  - The `read_value()` method returns the raw ADC value.
  - The `read_normal()` method returns a normalized integer value between 0-1000. 
- **Assigned to Help**:
  - **IR_Array.py**: calls this class for each sensor channel
  - **line_finder.py** / **line_task.py**: use data collected from this class to steer or detect line transitions

##### 6. PID.py
- **Purpose**: This class is a generic PID controller used by tasks requiring closed-loop control.
- **What It Does**:
  - In the `control(sp, pv, now)` method it calculates `error = sp - pv` and updates integral and derivative terms.
  - This method returns a control output `cv` used to set motor PWM or yaw rate.
- **Assigned to Help**:
  - **motorstask.py**: with speed or velocity control.
  - **line_task.py**: with offset correction for line following.
  - **grid_task.py**: feeds feeds dir to control heading.

#### 7. task_Bump.py
- **Purpose**: This class sets up the low-level bumper inputs, configuring interrupts or polling to detect contact.
- **What It Does**:
  - Initializes `ExtInt` objects on each bumper pin with `IRQ_FALLING`, meaning it now looks for a falling edge.
  - On interrupt this class calls `set_flag(line)` that sets `self.bump_state = True`.
- **Assigned to Help**:
  - **Collision_Detect_task.py**: uses this driver to read `get_button_state()` or `bump_state` to raise `bump_flg`.
  - **MM.py**: checks if the `bump_flg` indicating a collision needs to override the entire state machine.
 
#### 8. sensor_calibration.py
- **Purpose**: This class is a standalone script for calibrating the IR sensors, it runs offline to establish `white` and `black` thresholds.
- **What It Does**:
  - Logs and prints ADC values as the sensor hovers over black and white surfaces. 
  - User updates **IR_Sensor.py** based on these observed values.
- **Assigned to Help**:
  - **IR_Array.py** / **IR_Sensor.py**: helps these driver classes indirectly to produce accurate line detection data.
  - Important: Not used during normal robot operation—just a calibration tool.

## Finite State Machines

The following diagrams are a visual representation of each tasks finite state machine.

#### MM FSM

![MM 11](https://github.com/user-attachments/assets/245a1f70-c5f4-425f-8904-b5e9e69c22ad)

![MM 2](https://github.com/user-attachments/assets/95c17358-4c2b-4aaa-8179-8b3c09cc4449)

![MM 3](https://github.com/user-attachments/assets/1b38244d-e064-428d-9b46-d7b1c246c85d)

#### grid_task FSM

![grid task](https://github.com/user-attachments/assets/5f91b217-cb1e-4420-9249-c616d0ce81a1)

#### line_task FSM

![line follow](https://github.com/user-attachments/assets/c238e9e4-0c15-4e8a-94d3-598ce3675b60)

#### line_finder FSM

![line finder](https://github.com/user-attachments/assets/9c18f80f-a389-405b-bcb6-cc2b7017697d)

#### motortask FSM

![motor task](https://github.com/user-attachments/assets/811b49d9-0abc-4592-98b7-174e89465177)

#### Collision_Detect_task FSM

![collision task](https://github.com/user-attachments/assets/e364bd88-c75c-440a-bb5a-08f991e1fe5b)
