from pyb import Timer
from math import pi

class Encoder:
    '''A quadrature encoder decoding interface encapsulated in a Python class'''
    def __init__(self, tim, chA_pin, chB_pin):
        '''Initializes an Encoder object'''
        self.tim = tim # Timer passed from user. Frequency from lecture
        self.tim.channel(1, pin= chA_pin, mode=Timer.ENC_AB) #ERA
        self.tim.channel(2, pin= chB_pin, mode=Timer.ENC_AB) #ERB
        
        self.position = 0 # Total accumulated position of the encoder
        self.prev_count = 0 # Counter value from the most recent update
        self.delta = 0 # Change in count between last two updates
        self.deltas = [0, 0, 0, 0, 0] # list of last 5 deltas
        self.dt = 0 # Amount of time between last two updates
        self.dts = [0, 0, 0, 0, 0] # List of last 5 dts
        self.idx = 0 # Index to place last 5 points in
        self.prev_tim = 0
        self.AR = 0xFFFF # Autoreload Value
        
        self.r_w = 35 # Whell radius in [mm]
        
    def update(self, now):
        '''Runs one update step on the encoder's timer counter to keep
        track of the change in count and check for counter reload'''
        # Calculate Delta
        self.delta = self.tim.counter() - self.prev_count #update delta
        self.dt = now - self.prev_tim # update dt
        
        # Case of underflow
        if self.delta > (self.AR+1)/2:
            self.delta -= (self.AR + 1)
            
        # Case of overflow
        elif self.delta < -(self.AR+1)/2:
            self.delta += (self.AR+1)
        
        self.position += self.delta # Update Position
        self.deltas[self.idx] = self.delta # place delta into list of deltas
        self.dts[self.idx] = self.dt # Place dt into list of dts
        
        # Move the index to current pointer location
        if self.idx < 4:
            self.idx += 1
        else:
            self.idx = 0
            
        self.prev_count = self.tim.counter() # Current count becomes prev count
        self.prev_tim = now # update prev_tim
    
    def get_position(self):
        '''Returns the most recently updated value of position as determined
        within the update() method'''
        return self.position # Units of Ticks
    
    def get_lin_position(self):
        '''Returns most recently updated value of position in mm'''
        return (self.position*2*pi/1440)*self.r_w
    
    def get_velocity(self):
        '''Returns a measure of velocity using the the most recently updated
        value of delta as determined within the update() method'''
        # Calculate and return average velocity over last 5 updates
        return sum(self.deltas)*1_000_000 // sum(self.dts) # Units ticks/sec
    
    def zero(self, now):
        '''Sets the present encoder position to zero and causes future updates
        to measure with respect to the new zero position'''
        self.position = 0
        self.deltas = [0 ,0 ,0, 0, 0]
        self.dts = [0,0,0,0,0]
        self.prev_count = self.tim.counter()
        self.prev_tim = now