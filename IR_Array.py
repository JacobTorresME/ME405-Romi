from IR_Sensor import IR_Sensor
from pyb import Pin

class IR_Array:
    '''This class deals with the array of IR sensors'''
    def __init__(self):
        # Define all sensors
        self.IR_1 = IR_Sensor(Pin.cpu.C2, 2881, 334)
        self.IR_2 = IR_Sensor(Pin.cpu.C3, 2670, 311)
        self.IR_3 = IR_Sensor(Pin.cpu.A0, 2614, 304)
        self.IR_4 = IR_Sensor(Pin.cpu.A1, 2443, 293)
        self.IR_5 = IR_Sensor(Pin.cpu.A4, 2460, 298)
        self.IR_6 = IR_Sensor(Pin.cpu.B0, 2402, 295)
        self.IR_7 = IR_Sensor(Pin.cpu.C1, 2413, 293)
        self.IR_8 = IR_Sensor(Pin.cpu.C0, 2546, 295)
        self.IR_9 = IR_Sensor(Pin.cpu.A6, 2492, 298)
        self.IR_10 = IR_Sensor(Pin.cpu.A7, 2458, 291)
        self.IR_11 = IR_Sensor(Pin.cpu.C5, 2586, 299)
        self.IR_12 = IR_Sensor(Pin.cpu.B1, 2538, 299)
        self.IR_13 = IR_Sensor(Pin.cpu.C4, 2657, 311)
        # List including all 13 sensors
        self.sensor_list = [self.IR_1, self.IR_2, self.IR_3, self.IR_4, 
                            self.IR_5, self.IR_6, self.IR_7, self.IR_8,
                            self.IR_9, self.IR_10, self.IR_11, self.IR_12, 
                            self.IR_13]
        
        #Set up emittors
        self.ODD = Pin(Pin.cpu.C10, mode=Pin.OUT_PP) # Odd pin is tied to emmit
        self.ODD.high() # set emmitors high
        
        # Initialize threshold
        self.low_threshold = 3000
        self.high_threshold = 5000
        
        # Initialize the sums
        self.u_sum = 0# Unweighted Sum
        self.w_sum = 0 # Weighted sum
        
        
        self.centroid = 0 # Initialize centroid
        
    def update(self):
        '''Get unweighted and weighted sums of each senson reading'''
        # clear u_sum and w_sum
        self.u_sum = 0 
        self.w_sum = 0 
        
        # Iterate through all of the sensors
        for idx, sensor in enumerate(self.sensor_list, 1):
            sensor.update()
            value = sensor.read_normal() # get normalized value from senosr
            self.u_sum += value # Add value to unweighted sum
            value *= idx # Multiply value by index to get weighted value
            self.w_sum += value # Add weighted value to sum
        
    def get_centroid(self):   
        self.update()
        try:
            self.centroid = self.w_sum/self.u_sum # divide to get centroid
        except ZeroDivisionError:
            self.centroid = 0
        
        return self.centroid
    
    def find_line(self):
        '''This function will return 1 if romi detects that it is on a line
        and 0 if it is not on a line'''
        self.update() # Update sensor array sums
        
        # Check if it is on line
        if self.u_sum > self.high_threshold:
            # Case that the system is over something thicker than a line
            return 2 
        elif self.u_sum < self.low_threshold:
            # Case thate Romi is over something skinnier than a line
            return 1
        else:
            # Case that Romi is over a line
            return 0
        
    def test(self):
        '''This is used to return the unweighted sum to calibrate line
        thicknesses'''
        self.update()
        return self.u_sum
            
            
            
            