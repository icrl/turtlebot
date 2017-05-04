#!/bin/bash

import subprocess

# Runs the script that creates the grammar and retrieves the dictionary
subprocess.Popen(["python", "make_grammar.py"])

# Runs the script that creates the graphml graph
subprocess.Popen(["python", "write_graphml.py"])

# Runs roscore
subprocess.call(['gnome-terminal', '-x', 'bash', '-c','roscore'])

#Runs soundplay
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c','rosrun sound_play soundplay_node.py'])

# Runs pocketsphinx_continuous in a new terminal.  IF THE PATH TO GRAMMAR.JSGF OR TURTLEBOT_DIC.DIC CHANGES UPDATE THIS PATH
subprocess.call(['gnome-terminal', '-x', 'bash', '-c', 'cd /opt/ros/indigo/share/pocketsphinx/demo/Ourstuff/Movement_dialog; pocketsphinx_continuous -inmic yes -jsgf grammar.jsgf -dict turtlebot_dic.dic 2>./unwanted-stuff.log | tee ./words.log'])

# Runs the script that figures out the turtlebot's response to what was said in a new terminal.  IF THE PATH TO READ_GRAPH.PY CHANGES UPDATE THIS PATH
subprocess.call(['gnome-terminal', '-x', 'bash', '-c', 'cd /opt/ros/indigo/share/pocketsphinx/demo/Ourstuff/Movement_dialog; python navi_movements.py'])

print 'COMPLETE'
