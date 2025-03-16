from time import ticks_diff, ticks_us

class PID:
    
    def __init__(self, kp, ki, kd, k_ff):
        self.sp = 0 # setpoint
        self.pv = 0 # present value
        self.cv = 0 # control value
        self.integral = 0 # holds integral value
        self.prev_error = 0 # holds error from the last time controller was called
        self.prev_time = ticks_us() # holds previous time
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.kff = k_ff
        
    def control(self, sp, pv, now):
        try:
            '''Give a control vallue based on the present value'''
            dt = ticks_diff(now, self.prev_time)/1_000_000 # calculate how much time has passed [s]
            error = sp - pv
            # Use trapezoid rule to increase the integral
            self.integral += (error + self.prev_error)*dt/2
            # Calculate the derivative
            derivative = (error - self.prev_error)/dt
            
            # Control the system
            self.cv = self.kp*error + self.ki*self.integral + self.kd*derivative + self.kff*sp
            
            self.prev_time = now # make current time prev time for next run
        
            return self.cv
        
        except:
            return self.cv