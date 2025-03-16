from math import pi
from time import ticks_us

class motor_task:
    
    # Initializing motor and encoders
    def __init__(self, Motor, Encoder, K, PID):
        self.Motor = Motor
        self.PID = PID
        self.Encoder = Encoder
        self.K = K
        
    def generator(self, shares):
        # Unpack shares
        omega, run_flg = shares
        
        # Define Sate names
        S0_STANDBY = 0
        S1_RUN = 1
        state = 0 
       
        # Create forever loop
        while True:
            if state == S0_STANDBY:
                # Check run flag and transition on rising edge
                if run_flg.get() == 1:
                    state = S1_RUN # update state
                    self.Motor.enable() # enable motor
                    self.Encoder.zero(ticks_us())
                    print("Now I Run")
                    
            elif state == S1_RUN:
                # check for run flag and transition on falling edge
                if run_flg.get() == 0:
                    self.Motor.disable() # Disable motor on transition
                    state = S0_STANDBY
                # While running
                else:
                    now = ticks_us() # present time
                    self.Encoder.update(now) # Update encoder
                    pv = self.Encoder.get_velocity() # read velo from encoder
                    pv = pv*((2*pi)/1440) # convert velocity from ticks to rad
                    # use PID to choose effort and set on motor
                    sp = omega.get()
                    effort = self.PID.control(sp, pv, now)
                    if effort > 100:
                        effort = 100
                    elif effort < -100:
                        effort = -100
                    self.Motor.set_effort(effort)
                    
            yield 0 