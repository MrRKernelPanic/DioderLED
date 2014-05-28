from nanpy import Arduino
from nanpy import SerialManager
from time import sleep

#serial_manager.connect('/dev/ttyS0')        # serial connection to Arduino
connection = SerialManager()
a = Arduino(connection=connection)
a.pinMode(5, a.OUTPUT)

RLED = 5                        # LED on Arduino Pin 10 (with PWM)

print"Starting"
print"5 blinks"

for i in range(0,5):
    Arduino.digitalWrite(RLED, Arduino.HIGH)
    sleep(0.5)
    Arduino.digitalWrite(RLED, Arduino.LOW)
    sleep(0.5)

print"Changing brightness of LED"
bright = 128                           # Mid brightness
a.analogWrite(RLED, bright)

for i in range(0,200):
    bright = bright + 8
    if (bright > 200):          # LED already full on at this point
        bright = 0          # Minimum power to LED
    a.analogWrite(RLED, bright)           # Change PWM setting/brightness
    sleep(0.05)
a.digitalWrite(RLED,a.LOW)          # Turn off LED

print"Finished"
