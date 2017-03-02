#!/bin/bash

import subprocess
import shlex
import os
import time

subprocess.call(['killall', '-9', 'gnome-terminal'])
subprocess.call(['killall', '-9', 'rosmaster'])
time.sleep(3)
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c', 'roslaunch turtlebot_bringup minimal.launch'])
time.sleep(1)
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','rosrun sound_play soundplay_node.py'])
subprocess.call(['gnome-terminal', '-x', 'bash', '-c', 'cd /opt/ros/indigo/share/pocketsphinx/demo/Ourstuff; python 2ndDialog.py'])






#subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c', 'roscore'])
