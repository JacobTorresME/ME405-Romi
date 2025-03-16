from time import ticks_us

class grid_task:
    
    def __init__(self, my_IMU, IMU_PID, Left_Encoder, Right_Encoder):
        self.Left_Encoder = Left_Encoder
        self.Right_Encoder = Right_Encoder
        self.position = 0
        self.my_IMU = my_IMU
        self.IMU_PID = IMU_PID
        
        # Cardinal Directions
        self.North = 0
        self.South = 0 
        self.West = 0 
        
        self.state = 0
        self.length = 650 # Length of the tunnel
        
        # Encoder values for when the tunnel first starts
        self.left_start = 0 
        self.right_start = 0
        
        # State Names
        self.S0_INIT        = 0
        self.S1_STANDBY     = 1
        self.S2_TURN_SOUTH  = 2
        self.S3_DRIVE_SOUTH = 3
        self.S4_TURN        = 4
        self.S5_DRIVE_WEST  = 5
        
    def set_direction(self, heading):
        # Adjust heading to get a pv
        if heading < 2880:
            pv = - heading
        else:
            pv = 5760 - heading
        
        # Initializing the PID components
        sp = 0
        now = ticks_us()
        try:
            new_yaw_rate = self.IMU_PID.control(sp, pv, now)
        except:
            new_yaw_rate = 0
            
        return new_yaw_rate
        
        
    def generator(self, shares):
        yaw_rate, grid_flg, fwd_flg = shares
        
        while True:
            if self.state == self.S0_INIT:
                # Reading the sensor array to get the current euler angles
                heading, roll, pitch = self.my_IMU.read_eul_angles()
                # Set current heading to North
                self.North = heading
                # Set the other cardinal directions
                self.South = 2880
                self.West = 4320
                
                self.state += 1 # Increment state
                fwd_flg.put(0)
            elif self.state == self.S1_STANDBY:
                # Check for flag indicating it's time for the grid
                if grid_flg.get() == 1:
                    # Zero encoders on transition
                    # Set forward flag true on transition
                    # Increment state
                    self.state += 1 
                    
            elif self.state == self.S2_TURN_SOUTH:
                heading, roll, pitch = self.my_IMU.read_eul_angles()
                # Adjust heading to be in terms of west
                heading -= self.South
                # Ensure that heading remains positive
                if heading < 0:
                    heading += 5760
                if heading < 80:
                    fwd_flg.put(1) # Set fwd_flg on transition
                    self.state += 1 # Increment state
                    # Read encoders
                    self.left_start = self.Left_Encoder.get_lin_position()
                    self.right_start = self.Right_Encoder.get_lin_position()
                    yaw_rate.put(0)
                else:
                    # Turn to face west
                    yaw_rate.put(self.set_direction(heading))    
                    
            elif self.state == self.S3_DRIVE_SOUTH:
                # Get encoder positions (Encoders updated in motors task)
                # Make sure to subtract the offset from both encoder positions
                left_position = self.Left_Encoder.get_lin_position() - self.left_start
                right_position = self.Right_Encoder.get_lin_position() - self.right_start
                
                # Average linear position from left motor plus right motor
                lin_position = (left_position + right_position)/2
                
                # Check if Romi has reached the end of the tunnel
                if lin_position < self.length:
                    # Get euler angles
                    heading, roll, pitch = self.my_IMU.read_eul_angles()
                    
                    # Adjust heading to be in terms of south
                    heading -= self.South
                    # Ensure that heading remains positive
                    if heading < 0:
                        heading += 5760
                    # Set yaw rate according to this heading
                    yaw_rate.put(self.set_direction(heading))
                    
                else:
                    fwd_flg.put(0)
                    self.state += 1 # Increment state
        
                
            elif self.state == self.S4_TURN:
                heading, roll, pitch = self.my_IMU.read_eul_angles()
                # Adjust heading to be in terms of west
                heading -= self.West
                # Ensure that heading remains positive
                if heading < 0:
                    heading += 5760
                
                # Check if we are going West
                if heading < 80 or heading > 5700:
                    fwd_flg.put(1) # Set fwd_flg on transition
                    grid_flg.put(0)
                    yaw_rate.put(0)
                    self.state = 1

                else:
                    # Turn to face west
                    yaw_rate.put(self.set_direction(heading))
                    
            # elif self.state == self.S4_DRIVE_WEST:
            #     if grid_flg
            
            yield 0 
                    