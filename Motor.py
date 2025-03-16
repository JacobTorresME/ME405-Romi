from pyb import Pin, Timer

class Motor:
    '''A motor driver interface encapsulated in a Python class. Works with
    motor drivers using seperate PWM and direction inputs such as the DRV8838
    drivers present on the Romi chasis from Pololu.'''
    
    def __init__(self, PWM_ch, PWM_pin, DIR, nSLP):
        '''Initialize a Motor object'''
        self.nSLP_Pin = Pin(nSLP, mode=Pin.OUT_PP, value=0)
        self.DIR_Pin = Pin(DIR, mode=Pin.OUT_PP, value=0)
        self.tim = Timer(8, freq=20000) # Probably shouldn't reinitialize
        self.PWM_Pin = self.tim.channel(PWM_ch, pin=PWM_pin, mode=Timer.PWM)
    
    def set_effort(self, effort):
        '''Sets the present effort requested from the motor based on an input
        value between -100 and 100'''
        
        # Case for effort is positive
        if effort > 0:
            self.DIR_Pin.low() # makes the motor go forward
        # Case for effort is negative
        else:
            self.DIR_Pin.high() # Makes the motor go backward
            
        effort = abs(effort) # Ensure that effort is a positive value
            
        self.PWM_Pin.pulse_width_percent(effort) # Set PWM
    
    def enable(self):
        '''Enables the motor driver by taking it out of sleep mode into brake
        mode'''
        self.nSLP_Pin.high()
    
    def disable(self):
        '''Disables the motor driver by taking it into sleep mode'''
        self.nSLP_Pin.low() 