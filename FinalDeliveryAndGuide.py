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
    
goals = { "201": [-0.719,-0.14],
          "202": [1.8,0.523],
          "203": [4.92,0.701],
          "204": [8.75, 3.43],
          "205": [9.32,6.93],
	  "206": [3.9,5.89],
          "207": [1.25,2.43] }
          #"Door": [-2.98,1.66,0.404] }

class ttsconvert():

    def __init__(self):
        rospy.init_node('google', anonymous=False)
        rospy.loginfo('Initializing')
        #soundhandle = SoundClient(blocking=True)
        self.goal_sent = False
        self.tf = TransformListener()
        # What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)
        # Tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")
	# Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))
    
    def speak(self):
        sound_client = SoundClient()
        G = nx.read_graphml("/opt/ros/indigo/share/pocketsphinx/demo/Ourstuff/gSpeech.graphml",unicode)
        root = 'n1'
        current = root
        tracker = {'task': None, 'room': None}
	counter = 0
	output = None
        sound_client.playWave('/home/turtlebot/wavFiles/beep.wav', blocking=False)
        while True:
	    #counter = counter +1        
            # THE USER SPEAKS
            subprocess.call('./speech-rec.sh')
            # ANALYZE WHAT THE USER SAID
            f = open("words.log","r+")
            line = f.readline()
            #output = None
            if line:
                if line[0] in 't':
                    speech = line[12:].rstrip().lower()
		    print speech
	            if speech == "stop":
			break
		    see = -1
                    for e in G.edges(current, data=True):
                        expected = str(e[2].values()[0])
                        match = re.search(expected, speech)
                        if match or expected == 'room':
			    see = 1
                            current = e[1]
                            output = G.node[current]['dialogue']
                            if (expected=='guide'):                        
                                tracker['task']='guide'
                                break #out of for loop
                            elif (expected == 'deliver'):                
                                tracker['task']='deliver'
				tts = gTTS(text = 'Please place your item on top of my shell.', lang = 'en')
				tts.save('/home/turtlebot/wavFiles/item.wav')
				rospy.loginfo('Turtlebot says place you item...')
				sound_client.playWave('/home/turtlebot/wavFiles/item.wav', blocking=True)
                                break #out of for loop
              		    elif (expected == 'task'):
				if (tracker['task']=='deliver'):					
			            tracker['task']='guide'
			        elif (tracker['task']=='guide'):
				    tracker['task']='deliver'
				    tts = gTTS(text = 'Please place your item on top of my shell.', lang = 'en')
				    tts.save('/home/turtlebot/wavFiles/item.wav')
				    rospy.loginfo('Turtlebot says place you item...')
				    sound_client.playWave('/home/turtlebot/wavFiles/item.wav', blocking=True)
				tracker['room'] = str(room_number[0])
				output = output.replace('*', tracker['room'], 1)
				#if (tracker['task'] is not None):
			        output = output.replace('#', tracker['task'], 1) 	
		    
                            elif (expected == 'room'):
				if any(char.isdigit() for char in speech):
				    room_number = [int(s) for s in speech.split() if s.isdigit()]
				    if (room_number[0] < 201 or room_number[0] > 207):
					 tts = gTTS(text = 'The room is out of range. I can only go to room 201 to 207', lang = 'en')
					 tts.save('/home/turtlebot/wavFiles/oor.wav')
					 rospy.loginfo('Turtlebot says room out of range...')
					 sound_client.playWave('/home/turtlebot/wavFiles/oor.wav', blocking=True)
					 current = e[0]
					 output = G.node[current]['dialogue']	
				    else:
				        tracker['room'] = str(room_number[0])
				        output = output.replace('*', tracker['room'], 1)
				        #if (tracker['task'] is not None):
				        output = output.replace('#', tracker['task'], 1) 
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

	    '''else:
	        #tts = gTTS(text = 'Sorry, I did not understand that.', lang = 'en')
		#tts.save('/home/turtlebot/wavFiles/pardon.wav')
		rospy.loginfo('Turtlebot says I do not understand...')
		sound_client.playWave('/home/turtlebot/wavFiles/pardon.wav')'''
            
            # CHECK IF YOU HAVE TO GO OUT OF LOOP
            if (output == "Hold on! Let me calculate the path. Here I go!"):
                tts = gTTS(text = 'Byeeee', lang = 'en')
                tts.save('/home/turtlebot/wavFiles/bye.wav')
                rospy.loginfo('Turtlebot says end of conversation...')
                sound_client.playWave('/home/turtlebot/wavFiles/bye.wav', blocking=True)
                break
	    
        return tracker

    def goto(self, pos, quat):
	print "goto started"
	sound_client = SoundClient()
	#wait for sound_play to connect to publishers otherwise, it will miss first published psg
	rospy.sleep(3) #3 seconds?
	tts = gTTS(text = 'Going to destination', lang = 'en')
	tts.save("/home/turtlebot/wavFiles/goingTo.wav")

	self.move_base.max_vel_x = 0.25

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
	tracker = navigator.speak()
	room = tracker.get('room')
	position = {'x': goals.get(room, "201")[0], 'y':goals.get(room, "201")[1]}
        # Customize the following values so they are appropriate for your location
        #position = {'x': 5.12, 'y' : 2.72}
	if True:
	    quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

            #rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
            success = navigator.goto(position, quaternion)

            if success:
                rospy.loginfo("Hooray, reached the desired pose")
            else:
                rospy.loginfo("The base failed to reach the desired pose")
    except:
        rospy.loginfo("node terminated.")
