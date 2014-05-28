import time
 
from PyMata.pymata import PyMata
# Give the pins names:
REDPIN = 5
GREENPIN = 3
BLUEPIN = 6

FADESPEED = 5
 
# Create an instance of PyMata.
SERIAL_PORT = "/dev/ttyS0"
firmata = PyMata( SERIAL_PORT, max_wait_time=5 )
 
# initialize the digital pin as an output.
firmata.set_pin_mode( REDPIN, firmata.PWM, firmata.DIGITAL)
firmata.set_pin_mode( GREENPIN, firmata.PWM, firmata.DIGITAL)
firmata.set_pin_mode( BLUEPIN, firmata.PWM, firmata.DIGITAL) 

try:
    # run in a loop over and over again forever:
    while True:
        
        firmata.analog_write( BLUEPIN, 0 )
        for bright in range (0,255,8):
            firmata.analog_write( GREENPIN, bright )
            firmata.analog_write( REDPIN, bright )
#   firmata.analog_write( GREENPIN, 255 )
#   firmata.analog_write( BLUEPIN, 255 )
            time.sleep(0.1) # wait for a second
         
except KeyboardInterrupt:
 
    # Catch exception raised by using Ctrl+C to quit
    pass
 
# close the interface down cleanly
firmata.close()
