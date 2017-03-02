#!/bin/bash

import subprocess
import shlex
import os
import time

'''os.system("gnome-terminal -e 'bash -c \"roslaunch turtlebot_bringup minimal.launch\"'")

os.system("gnome-terminal -e 'bash -c \"rosrun sound_play soundplay_node.py\"'")
os.system("gnome-terminal -e 'bash -c \"roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/turtlebot/savedmaps/stations.yaml\"'")
os.system("gnome-terminal -e 'bash -c \"cd /opt/ros/indigo/share/pocketsphinx/demo/Ourstuff;python FinalDeliveryAndGuide.py \"'")'''
subprocess.call(['killall', '-9', 'gnome-terminal'])
subprocess.call(['killall', '-9', 'rosmaster'])
time.sleep(3)
#subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c', 'roscore'])
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c', 'roslaunch turtlebot_bringup minimal.launch'])
time.sleep(1)
#subprocess.Popen("roscore")
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','rosrun sound_play soundplay_node.py'])
time.sleep(1)
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/turtlebot/savedmaps/stations.yaml'])
subprocess.call(['gnome-terminal', '-x', 'bash', '-c', 'cd /opt/ros/indigo/share/pocketsphinx/demo/Ourstuff; python FinalDeliveryAndGuide.py'])
#subprocess.call(["rosrun", "sound_play", "soundplay_node.py"])
#subprocess.Popen(["python", "make_grammar.py"])
#subprocess.Popen(["python", "test.py"])
#subprocess.Popen(["python", "read_graph.py"])
#args = ('pocketsphinx_continuous', "-inmic", "yes", "-jsgf", "grammar.jsgf", "-dict", "turtlebot_dic.dic", "2>./unwanted-stuff.log", "|", "tee", "./words.log")
#cam2 = subprocess.Popen(['pocketsphinx_continuous', "-inmic", "yes", "-jsgf", "grammar.jsgf", "-dict", "turtlebot_dic.dic", "2>./unwanted-stuff.log", "|", "tee", "./words.log"], creationflags = subprocess.CREATE_NEW_CONSOLE)
#subprocess.call(['gnome-terminal', '-x', 'bash', '-c', 'cd /opt/ros/indigo/share/pocketsphinx/demo/Ourstuff; pocketsphinx_continuous -inmic yes -jsgf grammar.jsgf -dict turtlebot_dic.dic 2>./unwanted-stuff.log | tee ./words.log'])
#subprocess.call(['gnome-terminal', '-x', 'bash', '-c', 'cd /opt/ros/indigo/share/pocketsphinx/demo/Ourstuff; python read_graph.py'])


