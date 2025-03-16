# MM Task
from pyb import Pin, ExtInt
from time import ticks_us

class MM:
    
    def __init__(self, velocity, Left_Encoder, Right_Encoder, my_IMU, IMU_PID):
        self.button_state = False
        # Set up the button to flag on the falling edge when it is pushed
        self.user_button = ExtInt(Pin.cpu.C13, ExtInt.IRQ_FALLING, Pin.PULL_NONE, 
                            lambda line: self.set_flag(line))
        self.velocity = velocity # linear velocity of romi in m/s
        self.r_w = 0.035 # wheel radius in meters
        self.w = 0.163 # chassis width in meters
        
        # Mastermind will control the encoders
        self.Left_Encoder = Left_Encoder
        self.Right_Encoder = Right_Encoder
        
        # Set up the IMU stuff
        self.my_IMU = my_IMU
        self.IMU_PID = IMU_PID
        
        # Define Cardinal Directions
        self.North = 0 
        self.East = 5760/4
        self.South = 5760/2 
        self.West = 5760*3/4 
        
        self.state = 0 
        
    def set_flag(self, line):
        """Interrupt callback function to set when button pushed"""
        self.button_state = True  # Update the instance flag
        
    def decouple(self, fwd_flg, omega_r, omega_l, yaw_rate):
        '''This method takes in the omega and velocity and gives the each wheel
        the appropriate angular velocity to achieve that'''
        # determine linear velocity for decoupling matrix
        if fwd_flg.get() == 0:
            lin_velo = 0
        elif fwd_flg.get() == 2:
            lin_velo = -self.velocity
        elif fwd_flg.get() == 3:
            lin_velo = 0.75*self.velocity
        else:
            lin_velo = self.velocity
            
        # Use decoupling matrix to calculate what each wheel's velocity should be
        omega_r.put((1/self.r_w)*lin_velo + 
                    (self.w/(2*self.r_w))*yaw_rate.get())
        
        omega_l.put((1/self.r_w)*lin_velo - 
                    (self.w/(2*self.r_w))*yaw_rate.get())
        
    def check_stop(self, run_flg, bump_flg):
        '''This task check if the button has been pushed telling Romi to stop
        It returns 1 if a button has been pushed and returns 0 otherwise'''
        if self.button_state == True or bump_flg.get() == 1:
            print("I have been pushed")
            self.button_state = False # Clear button state
            run_flg.put(0) # Clear run flag
            bump_flg.put(0) # Clear the bump flag
            self.state = 0 # transition states
            print("stopping")
            return 1 
        else:
            return 0
        
    def update_position(self):
        # Read both encoders
        self.Left_Encoder.update(ticks_us())
        self.Right_Encoder.update(ticks_us())
        left_pos = self.Left_Encoder.get_lin_position()
        right_pos = self.Right_Encoder.get_lin_position()
        
        # Make the position the average of the two encoders
        return (left_pos + right_pos)/2
    
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
        # Unpack shares
        yaw_rate, omega_r, omega_l, grid_flg, fwd_flg, run_flg, line_follow_flg, line_flg, line_value, bump_flg = shares
        
        # Define Sate names
        S0_STANDBY       = 0
        S1_FIND_LINE     = 1
        S2_LEVEL_1       = 2
        S3_GRID_LEVEL    = 3
        S4_EXIT_TUNNEL   = 4
        S5_HITTING_WALL  = 5
        S6_MOV_BACK      = 6 
        S7_TURN_NORTH    = 7 
        S8_DRIVE_NORTH   = 8
        S9_TURN_WEST     = 9
        S10_DRIVE_WEST   = 10
        
         
        while True:
            if self.state == S0_STANDBY:
                # Check if the button was pressed
                if self.button_state == True:
                    self.button_state = False # Clear buttonstate
                    
                    ##### THIS IS FOR GRID TESTING
                    # Maybe come back to test grid
                    self.state += 1 # Advance state
                    
                    run_flg.put(1) # set run flg for the motors
                    fwd_flg.put(3) # Move at 3/4 speed
                    self.Left_Encoder.zero(ticks_us())
                    self.Right_Encoder.zero(ticks_us())
                    print("running")
                    
            elif self.state == S1_FIND_LINE:
                stop = self.check_stop(run_flg, bump_flg)
                
                if stop == 0:
                    ## Drive forward in a straight lilne
                    yaw_rate.put(0)
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    
                    # Check if we are on a line
                    if line_value.get(0) and self.update_position() > 100:
                        self.state += 1 # Increment state
                        line_follow_flg.put(1) # set flag for line follow task
                        fwd_flg.put(1)
                    
            elif self.state == S2_LEVEL_1:
                # This level 1 state follows the line up untill the grid
                # Check for stop
                stop = self.check_stop(run_flg, bump_flg)
                    
                # Button was not presssed
                if stop == 0:
                    # Run decoupling method
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    line_follow_flg.put(1)
                    # Check what line finder has found
                    if line_flg.get() == 1:
                        # Update encoder positions
                        position = self.update_position()
                        if position > 3500:
                            self.state += 1 # Increment state
                            # Zero both encoders on transition
                            self.Left_Encoder.zero(ticks_us())
                            self.Right_Encoder.zero(ticks_us())
                            line_follow_flg.put(0)
                            # Flag the grid on the transition 
                            grid_flg.put(1)
                            fwd_flg.put(0)
                            
                        else:
                            line_follow_flg.put(0)
                            yaw_rate.put(0)
                            
                            
                        # Clear the line_flg either way
                        line_flg.put(0)
                        
            elif self.state == S3_GRID_LEVEL:
                # This task runs through the grid 
                stop = self.check_stop(run_flg, bump_flg)
                if stop == 0:
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    if grid_flg.get() == 0:
                        self.state += 1 
                        self.Left_Encoder.zero(ticks_us())
                        self.Right_Encoder.zero(ticks_us())
                        
            elif self.state == S4_EXIT_TUNNEL:
                # This is the state for driving out of the tunnel
                stop = self.check_stop(run_flg, bump_flg)
                if stop == 0:
                    position = self.update_position()
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    if line_value.get() == 0 and position > 50:
                        line_follow_flg.put(1)
                        self.state += 1
                        
            elif self.state == S5_HITTING_WALL:
                # This is the state for driving on a line
                # I will pass the grid flag to stop because it is garanteed to
                # zero, and I do not want it to stop when it hits the wall
                stop = self.check_stop(run_flg, grid_flg) #chage bump flag to this
                if stop == 0:
                    # Check if the bumper has been hit
                    if bump_flg.get() == 1:
                        line_follow_flg.put(0)
                        fwd_flg.put(2) # This tells Romi to move backwards
                        yaw_rate.put(0)
                        bump_flg.put(0)
                        self.Left_Encoder.zero(ticks_us())
                        self.Right_Encoder.zero(ticks_us())
                        self.state += 1
                        #run_flg.put(1)
                    else:
                        self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                        
            elif self.state == S6_MOV_BACK:
                # This state is for moving backwards
                fwd_flg.put(2) # please work
                self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                position = self.update_position() # should this be lin?
                if position < -100:
                    self.state += 1
                    fwd_flg.put(0)
                    
            elif self.state == S7_TURN_NORTH:
                # This state is for turning North
                heading, roll, pitch = self.my_IMU.read_eul_angles()
                # Adjust heading to be in terms of west
                if heading < 70 or heading > 5700:
                    fwd_flg.put(1) # Set fwd_flg on transition
                    self.state += 1 # Increment state
                    # Read encoders
                    yaw_rate.put(0)
                else:
                    # Turn to face west
                    yaw_rate.put(self.set_direction(heading))
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    
            elif self.state == S8_DRIVE_NORTH:
                # Drive forward
                # Get euler angles
                heading, roll, pitch = self.my_IMU.read_eul_angles()
                # Set yaw rate according to this heading to point North
                yaw_rate.put(self.set_direction(heading))
                self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                position = self.update_position()
                if position >= 270:
                    self.state += 1
                    fwd_flg.put(0)
                    
            elif self.state == S9_TURN_WEST:
                # Turn West
                self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                heading, roll, pitch = self.my_IMU.read_eul_angles()
                # Adjust heading to be in terms of west
                heading -= self.West
                # Ensure that heading remains positive
                if heading < 0:
                    heading += 5760
                if heading < 70 or heading > 5700:
                    fwd_flg.put(1) # Set fwd_flg on transition
                    self.state += 1 # Increment state
                    # Stop moving and zero encoders
                    yaw_rate.put(0)
                    self.Left_Encoder.zero(ticks_us())
                    self.Right_Encoder.zero(ticks_us())
                else:
                    # Turn to face west
                    yaw_rate.put(self.set_direction(heading))  
                    
            elif self.state == S10_DRIVE_WEST:
                stop = self.check_stop(run_flg, grid_flg)
                if stop == 0:
                    heading, roll, pitch = self.my_IMU.read_eul_angles()
                    # Set yaw rate according to this heading to point North
                    yaw_rate.put(self.set_direction(heading-self.West))
                    # Drive forward until we hit the wall
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    position = self.update_position()
                    if position > 330:
                        fwd_flg.put(0)
                        self.state += 1
                    
            elif self.state == 11:
                # Turn South
                stop = self.check_stop(run_flg, grid_flg)
                if stop == 0:
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    heading, roll, pitch = self.my_IMU.read_eul_angles()
                    # Adjust heading to be in terms of west
                    heading -= self.South
                    # Ensure that heading remains positive
                    if heading < 0:
                        heading += 5760
                    if heading < 70 or heading > 5700:
                        fwd_flg.put(1) # Set fwd_flg on transition
                        self.state += 1 # Increment state
                        # Zero Encoders
                        self.Left_Encoder.zero(ticks_us())
                        self.Right_Encoder.zero(ticks_us())
                        # Set forward flag
                        fwd_flg.put(1)
                        yaw_rate.put(0)
                    else:
                        # Turn to face west
                        yaw_rate.put(self.set_direction(heading))  
                
                
            elif self.state == 12:
                # Drive forward
                stop = self.check_stop(run_flg, grid_flg)
                if stop == 0:
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    heading, roll, pitch = self.my_IMU.read_eul_angles()
                    # Set yaw rate according to this heading to point North
                    yaw_rate.put(self.set_direction(heading-self.South))
                    # Drive forward until we hit the wall
                    self.decouple(fwd_flg, omega_r, omega_l, yaw_rate)
                    position = self.update_position()
                    if position > 400:
                        fwd_flg.put(0)
                        self.state += 1
         
            else:
                run_flg.put(0)
                self.state = S0_STANDBY
                
               
                    
            yield 0