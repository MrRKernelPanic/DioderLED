import getpass
import logging
import struct
import time

from controlmypi import ControlMyPi
 
from PyMata.pymata import PyMata
# Give the pins names:
REDPIN = 5
GREENPIN = 3
BLUEPIN = 6

# Create an instance of PyMata.
SERIAL_PORT = "/dev/ttyS0"
firmata = PyMata( SERIAL_PORT, max_wait_time=5 )
 
# initialize the digital pin as an output.
firmata.set_pin_mode( REDPIN, firmata.PWM, firmata.DIGITAL)
firmata.set_pin_mode( GREENPIN, firmata.PWM, firmata.DIGITAL)
firmata.set_pin_mode( BLUEPIN, firmata.PWM, firmata.DIGITAL) 

def on_registered(conn):
    print "Registered with controlmypi.com!"
    
def on_control_message(conn, key, value):
    if key == 'echobox':
        print 'Received entry: %s' % value
        conn.update_status({'echo':'Pi echoes back: '+value})
    else:
        print key, value
	if key =='wheel':
		conn.update_status({'indicator':value})
		rgbstr=value[1:]
		rgb=struct.unpack('BBB',rgbstr.decode('hex'))
		print ('RGB VALUES:', rgb)
		firmata.analog_write( REDPIN, rgb[0])
		firmata.analog_write( GREENPIN, rgb[1])
		firmata.analog_write( BLUEPIN, rgb[2])		

def main_loop():
    # Block here. When you exit this function the connection to controlmypi.com will be closed
    raw_input("Press Enter to finish\n")

# Setup logging - change the log level here to debug faults
logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s %(message)s')

jid = "mark.routledge@gmail.com"
password = "oymwjqyzadqmvxcu"
id = "Test"
name = "DIODER COLOUR PICKER:"

panel_form = [
             	[ ['L','Echo box:'] ],
             	[ ['E','echobox','send'],['S','echo','-'],['W','wheel'],['I','indicator','#123456'] ]	
             ]

conn = ControlMyPi(jid, password, id, name, panel_form, on_control_message, 'hid', on_registered)
print "Connecting to ControlMyPi..."
if conn.start_control():
    try:
        main_loop()
    finally:
        conn.stop_control()
else:
    print("FAILED TO CONNECT")
