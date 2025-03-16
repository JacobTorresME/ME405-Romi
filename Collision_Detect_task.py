class collision_detection:
    
    def __init__(self, Bumper):
        self.Bumper = Bumper
        self.state = 0
        
    def generator(self, shares):
        # Unpacking shares 
        bump_flg = shares
        
        S0_WAIT_FOR_COLLISON    = 0
        S1_ACKNOWLEDGE_COLLISON = 1
        
        while True:
            if self.state == S0_WAIT_FOR_COLLISON:
                # Object used to check if bump has occurred
                bump = self.Bumper.get_button_state()
                # Check if one of the bumpers has been set
                if bump == True:
                    bump_flg.put(1) # Puts 1 in the bump flag for MM to see
                    self.state = S1_ACKNOWLEDGE_COLLISON
                    
            elif self.state == S1_ACKNOWLEDGE_COLLISON:
                # Checking if MM has cleared the flg
                if bump_flg.get() == 0:
                    # Go back to wait for collision state
                    self.Bumper.reset_button_state()
                    self.state = S0_WAIT_FOR_COLLISON
                    
            yield 0 
                
                    
                    
                
                
                
    
        