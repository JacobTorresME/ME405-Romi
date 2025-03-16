from pyb import Pin, ADC

class IR_Sensor:
    
    def __init__(self, dot, black, white):
        self.sensor = ADC(Pin(dot, mode=Pin.IN))
        self.black = black # This is the number for black line
        self.white = white # This is the number it sees for white lines
        self.value = 0 # Raw data ADC value from the sensor
        self.normal = 0 # Normalized 0 to 1000 value of sensor
    
    def update(self):
        '''Update sensor values'''
        # Update ADC value
        self.value = self.sensor.read()
        
        # Calculate Normal Value 0-1000
        # Case that value returned is lower than calibrated white, return white
        if self.value < self.white:
            self.normal = 0
        # Case that value is greater than calibrated black, return black
        elif self.value > self.black:
            self.normal = 1000
        # Case of value between white and black, normalize value
        else:
            self.normal = (self.value - self.white)*1000//(self.black
                                                           - self.white)
    
    def read_value(self):
        '''Return a raw ADC value of sensor reading'''
        return self.value # Return ADC value from sensor
    
    def read_normal(self):
        '''Return a normalized value where 1 is black and 0 is white'''
        return self.normal