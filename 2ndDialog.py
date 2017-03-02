#!/usr/bin/env python

'''
This handles the following tasks: 
draw a square: done 
follow: running only follwer.py doesn't work, also the tutorial says other ros commands shouldn't be running. pcall doesn't work but popen works,  however, running control c doesn't shut it so be careul!!. so i guess we could do that. also, https://www.youtube.com/watch?v=MbSs9fzI_tM we should probably ask the user to stand infront of the kinect before starting, also kinect dowen't work on gazebo
dance : done //left to add song 
follow voice commands goToDirection(foward, backward, left, right): done

@todo:
1. CHECK if follower.py works -> what if we copy all their code to this file?
2. download and extract 15sec of possible songs -> (dance: bad-michael jackson, sad: all by myself)
3. bring the speech part and this part together: since this works with pocketsphinx,i have almost no idea so...
'''

# An example of TurtleBot 2 drawing a 0.4 meter square.
# Written for indigo


# imports for draw a square

import re
import rospy
import networkx as nx
from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
from geometry_msgs.msg import Twist
from math import radians
from random import randint
from gtts import gTTS
import shlex, subprocess
import time
import os
import signal
import roslib; roslib.load_manifest('sound_play')

class Tasks():
    def __init__(self):
	rospy.init_node('drawasquare', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        rospy.loginfo('Initializing')
       
    def speak(self):
        sound_client = SoundClient()
        G = nx.read_graphml("/opt/ros/indigo/share/pocketsphinx/demo/Ourstuff/navi_move.graphml",unicode)
	print "here"
        root = 'n1'
        current = root                            
	output = G.node[current]['dialogue']
        tts = gTTS(text = output, lang = 'en')
        tts.save('/home/turtlebot/wavFiles/output.wav')
	rospy.loginfo('Turtlebot says I understood what you said...')
        sound_client.playWave('/home/turtlebot/wavFiles/output.wav', blocking=True)
	output = None

        while True:
	    #counter = counter +1        
            # THE USER SPEAKS
	    rospy.sleep(1)
            subprocess.call('./speech-rec.sh')
	
            # ANALYZE WHAT THE USER SAID
            f = open("words.log","r+")
            line = f.readline()
            #output = None
            if line:
                if line[0] in 't':
                    speech = line[12:].rstrip().lower()
		    print speech
	            if speech == "die":
			break
		    see = -1
                    for e in G.edges(current, data=True):
                        expected = str(e[2].values()[0])
                        match = re.search(expected, speech)
                        if match or expected == 'room':
			    see = 1
                            current = e[1]
                            output = G.node[current]['dialogue']
                            if (expected=='left'):      
				self.goToDirection('left')                  
                            elif (expected=='right'):
				self.goToDirection('right')                                          
                            elif (expected=='back'):     
				self.goToDirection('back')                                     
                            elif (expected=='forward'):    
				self.goToDirection('forward')                                      
			    elif (expected == 'follow me'):
				self.follower()
			    elif (expected == 'square'):
				self.drawSquare()
			    elif (expected == 'dance'):
				self.dance()			    
		    print "out of the loop"
	            if see < 0:
	                #tts = gTTS(text = 'Sorry, I did not understand that.', lang = 'en')
		        #tts.save('/home/turtlebot/wavFiles/pardon.wav')
		        rospy.loginfo('Turtlebot says I do not understand...')
		        sound_client.playWave('/home/turtlebot/wavFiles/pardon.wav', blocking=True)
		
	    if output:
            	tts = gTTS(text = output, lang = 'en')
            	tts.save('/home/turtlebot/wavFiles/output.wav')
            	rospy.loginfo('Turtlebot says I understood what you said...')
            	sound_client.playWave('/home/turtlebot/wavFiles/output.wav', blocking=True)
            
            # CHECK IF YOU HAVE TO GO OUT OF LOOP
            if (output == "Bye"):
		sound_client.playWave('/home/turtlebot/wavFiles/AllByMyself.wav', blocking=True)
                #tts = gTTS(text = 'Byeeee', lang = 'en')
                #tts.save('/home/turtlebot/wavFiles/bye.wav')
                rospy.loginfo('Turtlebot says end of conversation...')
                sound_client.playWave('/home/turtlebot/wavFiles/bye.wav', blocking=True)
                break
	    
        return tracker

    def drawSquare(self): 
        sound_client = SoundClient()
	#tts = gTTS(text = 'I am going to draw a square, please remove all obstacles around me. Thanks!', lang = 'en')
      	#tts.save('/home/turtlebot/wavFiles/square.wav')
       	rospy.loginfo('Turtlebot says I understood what you said...')
       	sound_client.playWave('/home/turtlebot/wavFiles/square.wav', blocking=True)
	count = 0
	while count <4:
	    count = count + 1
	    self.goToDirection("left")
	
    '''def follower(self):
        sound_client = SoundClient()
	tts = gTTS(text = 'I am going to follow you, here I come!', lang = 'en')
      	tts.save('/home/turtlebot/wavFiles/follow.wav')
       	rospy.loginfo('Turtlebot says I understood what you said...')
       	sound_client.playWave('/home/turtlebot/wavFiles/follow.wav', blocking=True)
	max_time = 30
	# The os.setsid() is passed in the argument preexec_fn so
	# it's run after the fork() and before  exec() to run the shell.
	follow = subprocess.Popen(["roslaunch", "turtlebot_follower", "follower.launch"])#, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)   
	#sound = subprocess.Popen(["rosrun", "sound_play", "soundplay_node.py"], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)     
	#rospy.sleep(10)
	start_time = time.time()  # remember when we started
	count = 0
	#soundhandle = SoundClient(blocking=False)
	#soundhandle.playWave('/home/turtlebot/wavFiles/dancesong.wav')
	while (time.time() - start_time) < max_time: 
	    #wait()
	    count = count +1
	    #print count

	os.killpg(os.getpgid(follow.pid), signal.SIGTERM)  # Send the signal to all the process groups
	print "killed successfully" 
	tts = gTTS(text = 'Whew! I am tired! You are sooooo fast', lang = 'en')
      	tts.save('/home/turtlebot/wavFiles/followEnd.wav')
       	rospy.loginfo('Turtlebot says I understood what you said...')
       	sound_client.playWave('/home/turtlebot/wavFiles/followEnd.wav', blocking=True)
	
	
	return None'''

    def dance(self):
	max_time = 25
    	sound_client = SoundClient(blocking=False)
    	# In the non-blocking version you need to sleep between calls.
        rospy.sleep(1)
	#PLAY THE SONG HERE
        rospy.loginfo('Playing the song, getting ready to dance')
	sound_client.playWave('/home/turtlebot/wavFiles/dancesong.wav')
    	rospy.sleep(1)
	#for some random number of times
	times = randint(4,7)
	count = 0
	start_time = time.time()  # remember when we started
	while (time.time() - start_time) < max_time:
	    #while (count < times):
	    count = count + 1
	    #generate random angle for dance
	    rad = randint(30, 120)		
	    self.turn('right', rad)
	    rangeDist = randint(3, 5)
	    self.goForward(rangeDist, 0.3)
	# turn or go forward 
	#tts = gTTS(text = 'Whew! I am tired! I think I will have to stop now!', lang = 'en')
      	#tts.save('/home/turtlebot/wavFiles/danceEnd.wav')
       	#rospy.loginfo('Turtlebot says I understood what you said...')
       	#sound_client.playWave('/home/turtlebot/wavFiles/danceEnd.wav', blocking=True)
	
    def goToDirection(self, direction):
	sound_client = SoundClient()
	'''tts = gTTS(text = 'I am moving now, please clear all obstacles around me!', lang = 'en')
      	tts.save('/home/turtlebot/wavFiles/goto.wav')
       	rospy.loginfo('Turtlebot says I understood what you said...')
       	sound_client.playWave('/home/turtlebot/wavFiles/goto.wav', blocking=True)'''
	
        self.turn(direction)
	self.goForward(rangeDist= 10, speed = 0.3)
        #self.turn(direction)

    def goForward(self, rangeDist = 10, speed = 0.2):

	# more info on http://wiki.ros.org/rospy/Overview/Time
        r = rospy.Rate(5)

	# create two different Twist() variables.  One for moving forward.  One for turning 45 degrees.
        # let's go forward at 0.2 m/s
        move_cmd = Twist()
        move_cmd.linear.x = speed
	# by default angular.z is 0 so setting this isn't required
	# goForward once. if we want the robot to go forward until it is stopped, 
	# may be in the original python file, run it once so that
	# turtlebot turns and move a little bit and then make it move forward
        # go forward 0.4 m (2 seconds * 0.2 m / seconds)
	rospy.loginfo("Going Straight")
        for x in range(0,rangeDist):
            self.cmd_vel.publish(move_cmd)
            r.sleep()

    def turn(self, direction, radAngle = 60):#default = 45 radians
        # 5 HZ
	# more info on http://wiki.ros.org/rospy/Overview/Time
        r = rospy.Rate(5)

        #let's turn at 45 deg/s
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(radAngle) #45 deg/s in radians/s : this angle might have to be changed -> doesn't turn complete 90 degrees all the time

	# how many radians should the turtlebot turn? since 1 turn = -90 degrees (counterclockwise 90) = 1 left turn
	numTurns = 0
	#direction should always be lowercase
	if direction=='left':
	    numTurns = 1
	if direction=='back':
	    numTurns = 2
	if direction=='right':
	    numTurns = 3
	
	# say the direction you're going
	# import gtts and say something like "i'm going in **direction"
	#two keep drawing squares.  Go forward for 2 seconds (10 x 5 HZ) then turn for 2 second
	count = 0
        
	# make that number of turns
	while count < numTurns:
	    count = count + 1
	    rospy.loginfo("Turning")
            for x in range(0,10):
                self.cmd_vel.publish(turn_cmd)
                r.sleep()

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop Drawing Squares")
        self.cmd_vel.publish(Twist())

 
if __name__ == '__main__':
    try:
	t = Tasks()
	#t.dance()
	t.speak()
	#t.follower()
        #rospy.loginfo(count)

    except:
        rospy.loginfo("node terminated.")

