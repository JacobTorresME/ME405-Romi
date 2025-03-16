from time import ticks_us

# Defining the line reading task
class line_task:
   
    # Initializationg obejcts in each method 
    def __init__(self, line_sensor, line_sensor_PID):
        self.line_sensor = line_sensor
        self.line_sensor_PID = line_sensor_PID
        self.state = 0
        
    def generator(self, shares):
        line_follow_flg, yaw_rate, fwd_flg = shares
        
        S0_STANDBY  = 0
        S1_RUN      = 1

        while True:
            
            if self.state == S0_STANDBY:
                # Wait for MM to set lff before incrementing states
                if line_follow_flg.get() == 1:
                    self.state += 1
                    fwd_flg.put(1) # Set forward flag on transition
            
            if self.state == S1_RUN:
                # Transition back to standby when the lff is cleared
                if line_follow_flg.get() == 0 :
                    self.state = S0_STANDBY
                    # fwd_flg.put(0) # Stop moving forward on transition
                    
                else:
                    # Reading the sensor array to get the centroid
                    centroid = self.line_sensor.get_centroid()
                    # Initializing the PID components
                    sp = 7
                    pv = centroid
                    now = ticks_us()
                    new_yaw_rate = self.line_sensor_PID.control(sp, pv, now)
                    yaw_rate.put(new_yaw_rate)
            
            yield 0

