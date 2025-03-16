# Bump Sensor Task
from pyb import Pin, ExtInt

class Bumper:
    
    def __init__ (self):
        self.bump_state = False
        # Setting up the bump sensor to flag on the falling edge when its pushed
        # PULL_NONe when its true its zero
        # IRQ look at the falling edge
        self.bump1 = ExtInt(Pin.cpu.H0, ExtInt.IRQ_FALLING, Pin.PULL_UP, lambda line: self.set_flag(line))
        self.bump2 = ExtInt(Pin.cpu.H1, ExtInt.IRQ_FALLING, Pin.PULL_UP, lambda line: self.set_flag(line))
        self.bump3 = ExtInt(Pin.cpu.C11, ExtInt.IRQ_FALLING, Pin.PULL_UP, lambda line: self.set_flag(line))
        self.bump4 = ExtInt(Pin.cpu.D2, ExtInt.IRQ_FALLING, Pin.PULL_UP, lambda line: self.set_flag(line))
    
    def set_flag(self, line):
        """Interupt callback function to set when bumper is pushed"""
        self.bump_state = True  # Update the instance flag
        
    def get_button_state(self):
        '''Returns bump sensor state state'''
        return self.bump_state
            
    def reset_button_state(self):
        '''resets button state to false'''
        self.bump_state = False # Reset the instance flag
        