import time
import math

from PyMata.pymata import PyMata

# Give the pins names:
REDPIN = 5
GREENPIN = 6
BLUEPIN = 3

# Create an instance of PyMata.
SERIAL_PORT = "/dev/ttyS0"
firmata = PyMata( SERIAL_PORT, max_wait_time=5 )

# initialize the digital pin as an output.
firmata.set_pin_mode( REDPIN, firmata.PWM, firmata.DIGITAL)
firmata.set_pin_mode( GREENPIN, firmata.PWM, firmata.DIGITAL)
firmata.set_pin_mode( BLUEPIN, firmata.PWM, firmata.DIGITAL)

def PosSinWave(amplitude, angle, frequency):
#angle in degrees
#creates a positive sin wave between 0 and amplitude*2
return amplitude + (amplitude * math.sin(math.radians(angle)*frequency) )


try:
# run in a loop over and over again forever:
while True:
  for n in range (0,720,5):
    r=PosSinWave(50, n, 0.5)
    g=PosSinWave(50, n, 1)
    b=PosSinWave(50, n, 2)

    #Write the colours to the pins.
    firmata.analog_write( REDPIN, int(r))
    firmata.analog_write( GREENPIN, int(g))
	 	firmata.analog_write( BLUEPIN, int(b))

    time.sleep(0.3) # wait for a bit

except KeyboardInterrupt:

  # Catch exception raised by using Ctrl+C to quit
  pass

# close the interface down cleanly
firmata.close()

