import rospy
import networkx as nx
import subprocess
from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest
from gtts import gTTS

class ttsconvert():

    def __init__(self):
        # initiliaze
        rospy.init_node('ttsconvert', anonymous=False)

	#rospy.loginfo('Example: Playing sounds in *blocking* mode.')
	soundhandle = SoundClient(blocking=True)

	#rospy.loginfo('Good Morning.')
	#soundhandle.playWave('/home/turtlebot/wavFiles/start.wav')

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)

	# Import the graphml to be read later
	G = nx.read_graphml("2nd_demo.graphml", unicode)
	#G = nx.read_graphml("/home/raeesa/networkx/examples/2nd_demo.graphml",unicode)
	#G = nx.read_graphml("/home/raeesa/Desktop/write_graphml.graphml",unicode)
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
	                        
				tts = gTTS(text = output, lang = 'en')
				tts.save('/home/raeesa/Desktop/line.wav')
                                
                                subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','pacmd set-source-mute 2 1'])
                                #subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','amixer set Capture nocap'])
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
		                
		        		# If there are no outgoing edges from the current node, go back to the root
				if G.out_degree(current) == 0:
					current = root

    def shutdown(self):
        rospy.loginfo("Stop")
	rospy.sleep(1)

if __name__ == '__main__':
    try: 
	ttsconvert()

    except:
	rospy.loginfo("node terminated")	    
	

