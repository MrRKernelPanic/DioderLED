from nanpy import Arduino
from nanpy import SerialManager
from time import sleep
from Tkinter import *
from tkColorChooser import askcolor

#serial_manager.connect('/dev/ttyS0')        # serial connection to Arduino
connection = SerialManager()
a = Arduino(connection=connection)
a.pinMode(5, a.OUTPUT)
a.pinMode(6, a.OUTPUT)
a.pinMode(3, a.OUTPUT)

RLED = 5                        # LED on Arduino Pin 10 (with PWM)
GLED = 3
BLED = 6

def setBgColor():
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        print (triple[0], " ", triple[1], " ", triple[2])
        a.analogWrite(RLED, triple[0])
        a.analogWrite(GLED, triple[1])
        a.analogWrite(BLED, triple[2])
        push.config(bg=hexstr)


print"Starting"
print"5 blinks"

a.digitalWrite(BLED,a.LOW)
a.digitalWrite(GLED,a.LOW)

for i in range(0,5):
    Arduino.digitalWrite(RLED, Arduino.HIGH)
    sleep(0.2)
    Arduino.digitalWrite(RLED, Arduino.LOW)
    sleep(0.2)

print"Changing brightness of LED"
bright = 128                           # Mid brightness
a.analogWrite(RLED, bright)
#a.digitalWrite(LED,a.HIGH)          # Turn on LED

for i in range(0,50):
    bright = bright + 8
    if (bright > 200):          # LED already full on at this point
        bright = 0          # Minimum power to LED
    a.analogWrite(RLED, bright)           # Change PWM setting/brightness
    sleep(0.05)

a.digitalWrite(RLED,a.LOW)          # Turn off LED
print"Finished"

root = Tk()
push = Button(root, text='Set Background Color', command=setBgColor)
push.config(height=3, font=('times', 20, 'bold'))
push.pack(expand=YES, fill=BOTH)
root.mainloop()
