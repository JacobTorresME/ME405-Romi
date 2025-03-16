# Test file for line sensors

from pyb import Pin
from time import ticks_us, ticks_diff, ticks_add
from IR_Sensor import IR_Sensor

# Create each IR class
IR_1 = IR_Sensor(Pin.cpu.C2, 2881, 334)
IR_2 = IR_Sensor(Pin.cpu.C3, 2670, 311)
IR_3 = IR_Sensor(Pin.cpu.A0, 2614, 304)
IR_4 = IR_Sensor(Pin.cpu.A1, 2443, 293)
IR_5 = IR_Sensor(Pin.cpu.A4, 2460, 298)
IR_6 = IR_Sensor(Pin.cpu.B0, 2402, 295)
IR_7 = IR_Sensor(Pin.cpu.C1, 2413, 293)
IR_8 = IR_Sensor(Pin.cpu.C0, 2546, 295)
IR_9 = IR_Sensor(Pin.cpu.A6, 2492, 298)
IR_10 = IR_Sensor(Pin.cpu.A7, 2458, 291)
IR_11 = IR_Sensor(Pin.cpu.C5, 2586, 299)
IR_12 = IR_Sensor(Pin.cpu.B1, 2538, 299)
IR_13 = IR_Sensor(Pin.cpu.C4, 2657, 311)

# Create an array with each of the IR sensors
IR_array = [IR_1, IR_2, IR_3, IR_4, IR_5, IR_6, IR_7, IR_8, IR_9, IR_10, IR_11, IR_12, IR_13]

ODD = Pin(Pin.cpu.C10, mode=Pin.OUT_PP) #Otuput of digital circuit/input to RC 

 # Set up software timing
interval = 500_000 # Time interval [us]
start = ticks_us() # Time of first run

# Initialize the deadline
deadline = ticks_add(start, interval) # first run deadline

# Turn on emitters
ODD.high()
 
# Run forever loop
while True:
    now = ticks_us() # Present time
    # if now is greater than deadline (our time interval)
    if ticks_diff(deadline, now) <= 0:
        for Sensor in IR_array:
            Sensor.update()
            # Print all normalized sensor readings on one line
            print(Sensor.read_normal(), end =", ")
        print()
        # Update deadline
        deadline = ticks_add(deadline, interval) # prep next deadline