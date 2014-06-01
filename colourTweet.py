import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import threading
import time
import textwrap
import subprocess
import struct

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
 
api_key='UHwGTldmoxrkECTaA4zGjeihZ'
api_secret='NYgslge6GvtvmBcLJUySm15WYahOpbFSu4AAuHWhd0VoIdrUOh'
 
access_token_key='2161868077-1aiRuSnYwTI24DoQ8Lkbx5pXsjj2d2vIVm4ArcA'
access_token_secret='ggwy8AA76JLlYo6uNbcdFbqdK7sFDw3zLsJIDXodABkc2'
 
 
class DisplayLoop(StreamListener):
    """
    This class is a listener for tweet stream data.
    It's also callable so it can run the main display 
    thread loop to update the display.
    """
    def __init__(self):
	self.colour_map = {'red':'REDDDDD',
                              'yellow':'YELLOWWWWWW',
                              'green':'GREEEEN',
                              'blue':'BLUUUUUUE',
                              'cyan':'CYANNNNNN',
                              'magenta':'MAGENTAAAAAA',
			      'rgb':'RGB',
			      'white':'WHITE'}

	self.msglist = []
        self.pos = 0
        self.tweet = 'Nothing yet'
         
    def set_colour(self):
        words = self.tweet.lower().split(' ')
        use_default = True
        for w in words[:]:
            if w in self.colour_map:
                print(self.colour_map[w])
                print(words.index(w))
		if(words[words.index(w)]=='rgb'):
			print(words[words.index(w)+1])
			#uptohere
			rgb=struct.unpack('BBB',words[words.index(w)+1].decode('hex'))
			print ('RGB VALUES:', rgb)
			firmata.analog_write( REDPIN, rgb[0])
			firmata.analog_write( GREENPIN, rgb[1])
			firmata.analog_write( BLUEPIN, rgb[2])
		elif (words[words.index(w)]=='red'):
			firmata.analog_write( REDPIN, 255)
                        firmata.analog_write( GREENPIN, 0)
                        firmata.analog_write( BLUEPIN, 0)
		elif (words[words.index(w)]=='green'):
                        firmata.analog_write( REDPIN, 0)
                        firmata.analog_write( GREENPIN, 255)
                        firmata.analog_write( BLUEPIN, 0)
		elif (words[words.index(w)]=='blue'):
                        firmata.analog_write( REDPIN, 0)
                        firmata.analog_write( GREENPIN, 0)
                        firmata.analog_write( BLUEPIN, 255)
		elif (words[words.index(w)]=='yellow'):
                        firmata.analog_write( REDPIN, 255)
                        firmata.analog_write( GREENPIN, 255)
                        firmata.analog_write( BLUEPIN, 0)
		elif (words[words.index(w)]=='magenta'):
                        firmata.analog_write( REDPIN, 255)
                        firmata.analog_write( GREENPIN, 0)
                        firmata.analog_write( BLUEPIN, 255)
		elif (words[words.index(w)]=='cyan'):
                        firmata.analog_write( REDPIN, 0)
                        firmata.analog_write( GREENPIN, 255)
                        firmata.analog_write( BLUEPIN, 255)
		elif (words[words.index(w)]=='white'):
                        firmata.analog_write( REDPIN, 255)
                        firmata.analog_write( GREENPIN, 255)
                        firmata.analog_write( BLUEPIN, 255)

		use_default = False
                break

        if use_default:
		print('LEDs set to white!!!')
                #SET THE LED COLOUR TO WHITE

    def on_data(self, data):
       	tweet_data = json.loads(data)
       	self.tweet = tweet_data['text'].encode('ascii',
                       errors='backslashreplace')
       	self.msglist = [x.ljust(16) for x in
                       textwrap.wrap(str(self.tweet),16)]
       	self.pos = 0
       	self.set_colour()
      	return True
 
    def on_error(self, status):
        print status
         
    def write_message(self,msg):
     	print (msg)

    def __call__(self):
        while True:
            time.sleep(1)
 
display_loop_instance = DisplayLoop()
 
# Start the thread running the callable
threading.Thread(target=display_loop_instance).start()
 
# Log in to twitter and start the tracking stream
auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token_key, access_token_secret)
stream = Stream(auth, display_loop_instance)
stream.filter(track=['AMC_PI'])
