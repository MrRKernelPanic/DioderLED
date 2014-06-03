#############################################################
#
#	Colour Changing Dioder LEDs by Tweet with response
#
#	This program will accept tweets sent to @AMC_PI or mentions of AMC_PI
#	It will then scan the tweet for 6 basic colours or the letters rgb!
#	It will then change the colour of the LED lights accordingly, reply 
#	with a friendly tweet and photographic evidence of the fact!
#	This program uses Tweepy and much of it was based on a couple of other
#	tutorials I cam across by Jeremy Blythe and Raspi.TV.  This is the first 
# 	time I haved used the Pi-Camera via Python and not the command line.
#	Unlike Jeremy Blythes example this program does not require you to use threading
#	which means you can just quite naturally without have to use 'ps ax' and then kill
# 	the process number.
#	
#	By Mark Routledge (Kernel Panic) 2nd June 2014
#
############################################################ 

import sys
import tweepy
import json
import time
import subprocess
import struct
import random
import picamera

#Basic Setup required for the Pi-Co-Op board driving the lights!
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

#Setting up the Twitter API with private keys etc.
#N.B.  To return tweets you must set the api on apps.twitter.com to read/write.
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Initialise the Pi Camera (N.B. It will turn the Pi camera LED on all the time!
camera = picamera.PiCamera()
camera.resolution = (1024, 768)

#Create a custom listener for twitter, the main crux of this program.
class CustomStreamListener(tweepy.StreamListener):
    #This is the main loop that does the testing when the 'listener picks up a tweet'
    def on_status(self, status):
	#Setup a basic list with terms to look for once it matches initial search.
	#N.B.  These should ALL be lower case as you flatten the tweet to .lower later.!!!
        colour_map = {'red':'REDDDDD',
                              'yellow':'YELLOWWWWWW',
                              'green':'GREEEEN',
                              'blue':'BLUUUUUUE',
                              'cyan':'CYANNNNNN',
                              'purple':'MAGENTAAAAAA',
                              'rgb':'RGB',
                              'white':'WHITE'}
	#Print out the initial tweet, unaltered.
	print status.text
	# Currently status.text is UNICODE, must convert to ASCII!!!
	to_test=status.text.encode('ascii'
		,errors='backslashreplace')
	#Break the tweet down into WORDS seperated by spaces.
	words = to_test.lower().split(' ')
	#Prints out the list of seperate words in the tweet.
	print words
	#Go through each of the words in the list trying to match them with the colour_map
	for w in words[:]:
            if w in colour_map:
		#if it matches then print out the colour response and the word position.
                print(colour_map[w] + ' ' + words.index(w))
                #Test if they used rgb value and handle the NEXT word in the list.
		if(words[words.index(w)]=='rgb'):
                	print(words[words.index(w)+1])
                        #Assume the RGB value passed as hex code without '#'
			#convert these values to a tuple of 3x number values.
			rgb=struct.unpack('BBB',words[words.index(w)+1].decode('hex'))
                        #Print out the r,g,b values.
			print ('RGB VALUES:', rgb)
			#Write the colours to the pins.
                        firmata.analog_write( REDPIN, rgb[0])
                        firmata.analog_write( GREENPIN, rgb[1])
                        firmata.analog_write( BLUEPIN, rgb[2])
		#Test for the obvious 6x Colours and WHITE!
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
                elif (words[words.index(w)]=='purple'):
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
	
	#Print out the username of the TWEETER!
	print status.user.screen_name
	#Start the camera preview and take a snap as image.jpg!
	camera.start_preview()
	camera.capture('image.jpg')
	time.sleep(1)
	camera.stop_preview()
	
	#Create a random number between 1 and 42, 
	#I did this as multiple IDENTICLE posts to the same user are not allowed!
	x=str(random.randint(1,42))
        api.update_with_media('image.jpg',"\nThanks " + status.user.screen_name + "\n \n Your lucky number for today is " + x, in_reply_to_status_id = status.id)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

#Create the instance of the custom 'LISTENER' and what to monitor.
sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['@AMC_PI'])
