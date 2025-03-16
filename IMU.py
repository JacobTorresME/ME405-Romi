from pyb import I2C, Pin
import struct
import time

## IMU Driver Class

class IMU:
    
    def __init__(self, RST_PIN):
        # Initialize I2C
        self.i2c = I2C(2, I2C.CONTROLLER)
        self.addr = 0x28
        self.RST_PIN = RST_PIN
        
    def reset(self):
        self.RST_PIN.low()
        time.sleep(0.1)
        self.RST_PIN.high()
        time.sleep(0.7)  # Wait for reset to complete
        
    def choose_mode(self, cmd):
        '''This sets the IMU to one of the fusion modes'''
        OPR_MODE = 0x3D
        # Set the mode depending on what mode was selected in cmd
        # Reg values found on page 21 of BNO055 Data Sheet
        if cmd == 'IMU':
            mode = 0x18
        elif cmd == 'COMPASS':
            mode = 0x19
        elif cmd == 'M4G':
            mode = 0x1A
        elif cmd == 'NDOF_FMC_OFF':
            mode = 0x1B
        elif cmd == 'NDOF':
            mode = 0x1C
        elif cmd == 'CONFIG':
            mode = 0
        else:
            raise TypeError("Incorrect Mode Chosen")
            
        # Write the mode to the I2C
        self.i2c.mem_write(mode, self.addr, OPR_MODE, timeout=1000)
        
    def read_cal_status(self):
        '''This reads the calibration statuses'''
        CALIB_STAT = 0x35 # Memory address of calibration status
        # Read memory status bit
        calib_status = self.i2c.mem_read(1, self.addr, CALIB_STAT)
        
        # Extract individual calibration statuses
        # Returns 1 if calibrated and 0 if not
        sys = 1 if ((calib_status[0]>> 6) & 0x03) == 3 else 0
        gyro = 1 if ((calib_status[0]>> 4) & 0x03) == 3 else 0
        accel =  1 if((calib_status[0]>> 2) & 0x03) == 3 else 0
        mag =  1 if(calib_status[0] & 0x03) == 3 else 0
        
        return sys, gyro, accel, mag
    
    def scan(self):
        yo = self.i2c.scan()
        return yo
    
    def read_cal_coefficients(self):
        '''retrieve the calibration coefficiens''' 
        # Must be placed in configuration mode
        self.choose_mode('CONFIG')
        time.sleep(0.2)
        # data = bytearray(0 for n in range(22))
        data = self.i2c.mem_read(22, self.addr, 0x55)
        
        # Return back to the other mode
        self.choose_mode('IMU')
        time.sleep(0.1)
        return data
        
    def write_cal_coefficients(self, data_list):
        '''write calibration coefficients from a list of 18 bytes stored in
        data'''
        # Create a byte array that holds all of the data
        data = bytearray(0 for i in range(22))
        for i, item in enumerate(data_list):
            data[i] = item
        
        # Place IMU into CONFIG mode
        self.choose_mode('CONFIG')
        time.sleep(0.2)
        
        # Write coefficients
        self.i2c.mem_write(data, self.addr, 0x55)
        
        # Return IMU to NDOF mode
        self.choose_mode('IMU')
        time.sleep(0.1)
        
    def read_eul_angles(self):
        '''Read eueler angles from IMU'''
        # Create a byte array for the data
        eul_angles = bytearray(0 for n in range(6))
        # Read from the propper register
        self.i2c.mem_read(eul_angles, self.addr, 0x1A)
        # Unpack byte array
        heading, roll, pitch = struct.unpack("<hhh", eul_angles)
        
        return heading, roll, pitch
        
    def read_angular_velocity(self):
        '''Read angular velocity from IMU'''
        # Create a byte array for the data
        ang_velos = bytearray(0 for n in range(6))
        # Read from the propper register
        self.i2c.mem_read(ang_velos, self.addr, 0x1A)
        # Unpack byte array
        ang_x, ang_y, ang_z = struct.unpack("<hhh", ang_velos)
        
        return ang_x, ang_y, ang_z
        
        
        
        