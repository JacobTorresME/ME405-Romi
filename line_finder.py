class line_finder:
    
    def __init__(self, IR_ARRAY):
        self.IR_ARRAY = IR_ARRAY
        self.state = 0
        
    def generator(self, shares):
        # Unpack shares
        line_flg, line_value = shares
        
        S0_LOOK_FOR_LINE    = 0
        S1_LOOK_FOR_ACK     = 1
        
        while True:
            if self.state == S0_LOOK_FOR_LINE:
                # Check line array to see if line is detected
                line = self.IR_ARRAY.find_line()
                # Check if a line is detected
                line_value.put(line) # Share what the line is
                if line > 0:
                    line_flg.put(1) # Flag MM that we are not over a line
                    print("I am not on a line")
                    self.state = S1_LOOK_FOR_ACK
                    
            elif self.state == S1_LOOK_FOR_ACK:
                # Check if MM has cleared the line flag
                if line_flg.get() == 0:
                    # Transition states
                    self.state = S0_LOOK_FOR_LINE
                # Still update line_value here
                line = self.IR_ARRAY.find_line()
                line_value.put(line)
            
            yield 0
        
        