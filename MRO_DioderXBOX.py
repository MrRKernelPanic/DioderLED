# pygame example: github.com/pddring/pygame-examples

import pygame
import random
import time
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

# wait for the user to press a key and return the keycode
def wait_for_key():
    e = pygame.event.wait()
    while e.type != pygame.KEYDOWN:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            return pygame.K_ESCAPE
    return e.key


# show the pygame window
pygame.init()
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption("Pygame Example")
# loop around until the user presses escape or Q
looping = True
red = 0
green = 0
blue = 0

while looping:

    # fill the screen in the random colour
    screen.fill((red, green, blue))
    pygame.display.flip()
    firmata.analog_write( REDPIN, red )
    firmata.analog_write( GREENPIN, green )
    firmata.analog_write( BLUEPIN, blue )

    # wait for a key to be pressed
    key = wait_for_key()
    
    # Test for Xbox Pad Buttons
    if key == pygame.K_b:
        red=red+8
        if red>255:
            red=0

    if key == pygame.K_a:
        green=green+8
        if green>255:
            green=0

    if key == pygame.K_x:
        blue=blue+8
        if blue>255:
            blue=0

    # stop looping if the user presses Q or escape
    if key == pygame.K_q or key == pygame.K_ESCAPE:
        looping = False
        firmata.close()
        pygame.quit()
