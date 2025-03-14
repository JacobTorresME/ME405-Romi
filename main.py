## Main Program for Lab 0x04

import gc
from pyb import Pin, Timer
import cotask
import task_share
from array import array
from Motor import Motor
from Encoder import Encoder
from time import ticks_us, ticks_diff, sleep
from motorstask import motor_task
from IR_Array import IR_Array
from line_task import line_task
from PID import PID
from MM import MM
from IMU import IMU
from task_IMU import task_IMU
from grid_task import grid_task
from line_finder import line_finder
from task_Bump import Bumper
from Collision_Detect_task import collision_detection

# Iniate all motors and sensors
# Motors
Left_Motor = Motor(4, Pin.cpu.C9, Pin.cpu.A10, Pin.cpu.B8)
Right_Motor = Motor(3, Pin.cpu.C8, Pin.cpu.B2, Pin.cpu.C6)
K_l = 6.73 # Left Motor constant rad/[s-vot]
K_r = 6.39 # Right Motor Constant radd/(s-volt)
# Encoders
Left_Encoder = Encoder(Timer(3, period=0xFFFF, prescaler=0), 
                       Pin.cpu.B4, Pin.cpu.B5)
Right_Encoder = Encoder(Timer(1, period=0xFFFF, prescaler=0), 
                         Pin.cpu.A8, Pin.cpu.A9)
# Line Sensor
line_sensor = IR_Array()

# IMU
# Set up Pins for IMU
Pin(Pin.cpu.B10, mode = Pin.OUT)
Pin(Pin.cpu.B11, mode = Pin.OUT)
IMU_RST = Pin(Pin.cpu.B15, mode = Pin.OUT)
Pin(Pin.cpu.B13, mode = Pin.ALT, alt = 4)
Pin(Pin.cpu.B14, mode = Pin.ALT, alt = 4)


# Create an IMU object
my_IMU = IMU(IMU_RST)

# Reset Romi for safe measure
my_IMU.reset()

# Place IMU into fusion mode
my_IMU.choose_mode('IMU')

# Create a data list with all of the calibration coefficients
data_list = [227, 255, 47, 0, 238, 255, 22, 3, 20, 255, 8, 3, 0, 0, 0, 0, 0, 0, 232, 3, 38, 2]
my_IMU.write_cal_coefficients(data_list)

print("hello")
print(my_IMU.read_cal_status())
data = my_IMU.read_cal_coefficients()
sleep(0.1)
data_list2 = list(data)
print(data_list2)

heading, roll, pitch = my_IMU.read_eul_angles()
print(f"heading: {heading}, roll: {roll} pitch: {pitch}")

# PIDs
IMU_PID = PID(0.004, 0, 0, 0)
line_sensor_PID = PID(0.6, 0.06, 0.0, 0) #0.6 .065, .4 .08
left_motor_PID = PID(10, 10, 0, 100/(K_l*4.5))
right_motor_PID = PID(10, 10, 0, 100/(K_r*4.5))
# Misc Variables
velocity = 0.2

# Creating bumper objects
Bump_sensor = Bumper()

# Initiate Task Objects
task1_MM = MM(velocity, Left_Encoder, Right_Encoder, my_IMU, IMU_PID)
task2_right_motor = motor_task(Right_Motor, Right_Encoder,K_r, right_motor_PID)
task3_left_motor = motor_task(Left_Motor, Left_Encoder, K_l, left_motor_PID)
task4_grid = grid_task(my_IMU, IMU_PID, Left_Encoder, Right_Encoder)
task5_line_follow = line_task(line_sensor, line_sensor_PID)
task6_line_finder = line_finder(line_sensor)
task7_wall_task = collision_detection(Bump_sensor)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a shares to pass between tasks
    yaw_rate = task_share.Share('f', thread_protect=False, name="yaw_rate")
    omega_r = task_share.Share('f', thread_protect=False, name="omega_r")
    omega_l = task_share.Share('f', thread_protect=False, name="omega_l")
    run_flg = task_share.Share('i', thread_protect=False, name="run_flg")
    grid_flg = task_share.Share('i', thread_protect=False, name="grid_flg")
    fwd_flg = task_share.Share('i', thread_protect=False, name="fwd_flg")
    line_follow_flg= task_share.Share('i', thread_protect=False, name="line_follow_flg")
    line_flg = task_share.Share('i', thread_protect=False, name="line_flg")
    line_value = task_share.Share('i', thread_protect=False, name="line_value")
    bump_flg = task_share.Share('i', thread_protect=False, name="bump_flg")
    

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_MM.generator, name="Task_1", priority=10, period=10,
            profile=True, trace=False, shares=(yaw_rate, omega_r, omega_l, 
                    grid_flg, fwd_flg, run_flg, line_follow_flg, line_flg, line_value, bump_flg))
    
    task2 = cotask.Task(task2_right_motor.generator, name="Task_2",
                        priority=4, period=10, profile=True, trace=False, 
                        shares=(omega_r, run_flg))
    task3 = cotask.Task(task3_left_motor.generator, name="Task_3", priority=4, period=10,
            profile=True, trace=False, shares=(omega_l, run_flg))
    task4 = cotask.Task(task4_grid.generator, name="Task_4", priority=4, period=10,
            profile=True, trace=False, shares=(yaw_rate, grid_flg, fwd_flg))
    task5 = cotask.Task(task5_line_follow.generator, name="Task_5", priority=3, period=10,
            profile=True, trace=False, shares=(line_follow_flg, yaw_rate, fwd_flg))
    task6 = cotask.Task(task6_line_finder.generator, name="Task_6", priority=1, period=10,
            profile=True, trace=False, shares=(line_flg, line_value))
    task7 = cotask.Task(task7_wall_task.generator, name="Task_7", priority=9, period=10,
            profile=True, trace=False, shares=(bump_flg))
    
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)
    cotask.task_list.append(task5)
    cotask.task_list.append(task6)
    cotask.task_list.append(task7)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            Left_Motor.disable()
            Right_Motor.disable()
            break
        except Exception as e:
            Left_Motor.disable()
            Right_Motor.disable()
            print(e)
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    # print(task1.get_trace())
    print('')