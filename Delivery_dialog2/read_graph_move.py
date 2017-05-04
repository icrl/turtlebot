 #!/bin/bash
''' = constraineD_google_dialogue + go_to_a_specific_point.py'''
import shlex, subprocess
import re
import rospy
import networkx as nx
from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
from gtts import gTTS
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import roslib; roslib.load_manifest('sound_play')
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
import time
from gtts import gTTS
from tf import TransformListener


    
goals = { "two hundred one": [-0.719,-0.14],
          "two oh one": [-0.719,-0.14],
          "two hundred two": [1.8,0.523],
          "two oh two": [-0.719,-0.14],
          "two hundred three": [4.92,0.701],
          "two oh four": [-0.719,-0.14],
          "two hundred four": [8.75, 3.43],
          "two oh five": [-0.719,-0.14],
          "two hundred five": [9.32,6.93],
          "two oh six": [-0.719,-0.14],
	  "two hundred six": [3.9,5.89],
          "two oh seven": [-0.719,-0.14],
          "two hundred seven": [1.25,2.43] }
          #"Door": [-2.98,1.66,0.404] }

class ttsconvert():
    
    def __init__(self):
        tracker = {'room': None}
        # initiliaze
        rospy.init_node('ttsconvert', anonymous=False)
        self.tf = TransformListener()
	#rospy.loginfo('Example: Playing sounds in *blocking* mode.')
	soundhandle = SoundClient(blocking=True)
        self.goal_sent = False
	#rospy.loginfo('Good Morning.')
	#soundhandle.playWave('/home/turtlebot/wavFiles/start.wav')
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")
	# Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))
        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)

	# Import the graphml to be read later
	G = nx.read_graphml("2nd_demo.graphml", unicode)
	root = 'n1'
	current = root

	# Clear words.log
	f = open("words.log","r+")
	f.seek(0)
	f.truncate()

	# Clear clean.log
	with open("clean.log", "w"):
	    pass

	# Constantly read from words.log for new lines
	while True:
	    line = f.readline()
	    
	    # If the user said something
	    if line:
		# The lines with dialogue all begin with a numerical value
		if line[0][:1] in '0123456789':
		    # remove 9 numbers, colon, and space from the beginning, and any whitespace from the end of the line
		    speech = line[11:].rstrip()
		    print speech
		        
                    count = 0
		    # Search through all edges connected to the current node
		    for e in G.edges(current, data=True):
		        
		        # If what was spoken matches the 'spoken' attribute of the edge
			if str(speech) == str(e[2].values()[0]):
		        	# Switch the current node to be the node the edge goes to
				current = e[1]
		                
                                # find '*' symbol in output string and and replace it with what user said stored in speech

		        	# Get the dialogue stored in the new node and save it in 'output'
				output = G.node[current]['dialogue']
                                if current=='n7':
                                        output = output.replace('*', str(speech))
                                        tracker['room'] = str(speech).lower()
				print 'OUTPUT: %s' %output
	                        
				tts = gTTS(text = output, lang = 'en')
				tts.save('/home/raeesa/Desktop/line.wav')
                                
                                subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','pacmd set-source-mute 2 1'])
				#rospy.loginfo('playing output')
				soundhandle.playWave('/home/raeesa/Desktop/line.wav', blocking = True)
	    			#soundhandle.say(output)
		                subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','pacmd set-source-mute 2 0'])

		        	# Add 'output' to the top of clean.log
				with open("clean.log","r+") as g:
		            		# Read everything from clean.log into 'content'
					content = g.read()
		            		# Go to the top of the file
					g.seek(0,0)
		            		# Write 'output' with 'content' appended to the end back to clean.log
		            		g.write(output.rstrip('\r\n')+'\n'+content)
		            		g.close()

                                if current == 'n9':
                                        room = tracker.get('room')
	                                position = {'x': goals.get(room, "201")[0], 'y':goals.get(room, "201")[1]}
                                        # Customize the following values so they are appropriate for your location
                                        #position = {'x': 5.12, 'y' : 2.72}
                                        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

                                        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
                                        self.goto(position, quaternion)
		                
		        		# If there are no outgoing edges from the current node, go back to the root
				if G.out_degree(current) == 0:
					current = root

    def goto(self, pos, quat):
	print "goto started"
	sound_client = SoundClient()
	#wait for sound_play to connect to publishers otherwise, it will miss first published psg
	rospy.sleep(3) #3 seconds?
	tts = gTTS(text = 'Going to destination', lang = 'en')
	tts.save("/home/turtlebot/wavFiles/goingTo.wav")
        # Send a goal
        self.goal_sent = True
	if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
            t = self.tf.getLatestCommonTime("/base_link", "/map")
            position, quaternion = self.tf.lookupTransform("/base_link", "/map", t)
	    rospy.loginfo(position[0])

	goal = MoveBaseGoal()
	#if(os.path.isfile("/home/wavFiles/goingTo.wav") == False)
	#the path to gtts-cli.py might have to be changed based on setup

        #play the wav file
	rospy.loginfo("Playing goingTo.wav")
        sound_client.playWave("/home/turtlebot/wavFiles/goingTo.wav")
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(120)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
	    tts = gTTS(text = 'Yay, reached destination', lang = 'en')
	    tts.save("/home/turtlebot/wavFiles/reachedTo.wav") 
	    
    	    sound_client.playWave("/home/turtlebot/wavFiles/reachedTo.wav")
	
        
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
	
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        #ttsconvert()
        navigator = ttsconvert()#GoToPose()
    except:
        rospy.loginfo("node terminated.")
