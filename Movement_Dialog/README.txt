Package contains all the files to compile a dictionary, grammar and graphml and run Pocketsphinx voice recognition. Type python ./run_scripts.py in the terminal to execute the program.

Description of all the files:
1. read_from.txt - Contains the spoken input and turtlebot reponse. The spoken input is written in a grammar format. EDIT HERE IF YOU WANT TO ADD MORE WORDS TO THE DICT.
2. make_grammar.py - Reads from the read_from.txt and converts the spoken input to a grammar script format. It also runs sphinxjsgf2fsg (which is in usr/bin), fsg2wlist.perl (to convert fsg to word file) and get_dict.py (to convert word file to dictionary).
3. grammar.jsgf - Grammar script for spoken input. DO NOT EDIT. File is always overwritten.
4. grammar.fsg - Converted from jsgf. Grammar script for spoken input. DO NOT EDIT. File is always overwritten.
5. grammar.word = Converted from fsg. Grammar script for spoken input. DO NOT EDIT. File is always overwritten.
6. fsg2wlist.pl - It convert fsg to words. DO NOT DELETE OR EDIT.
7. get_dict.py - It uses Selenium to upload the .word file to the online lmtool  and downloads the dictionary.
*8. test.py - Reads from read_from.txt and writes it into a graphml file.
9. turtlebot_dic.dic - Dictionary for turtlebot. Words in it are recognized by the turtlebot. DO NOT EDIT.
10. read_graph.py - Gets the spoken sentence and reads the graphml file to find what the turtlebot response should be. 
11. run_scripts.py - Executes all the python programs and starts pocketsphinx.
12. words.log - Displays output from pocketsphinx_continuous terminal.
13. unwanted_stuff.log - Garbage from pocketsphinx_continuous terminal.
14. clean.log - The turtlebot response is printed here. Latest response goes to the first line.

DEPENDENCIES:
Pocketsphinx(specifically pocketsphinx_continuous and sphinx_jsgf2fsg), NetworkX, Selenium, chromedriver and Chrome
