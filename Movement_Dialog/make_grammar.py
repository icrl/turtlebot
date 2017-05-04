import subprocess

# Read everything from readfrom.txt
f = open("navi_move.txt","r")
lines = f.readlines()
f.close()

# Keeps track of the number of rules added.
num = 0

# Header of the file
text = "#JSGF V1.0;\ngrammar hello;\n"

# Transforms each line from the text file into grammar rules.  'num' keeps track of how many rules were created.
end = False
for line in lines:
    if end == True and line.strip() != "":
        text = text + "<" + str(num) + "> = "
        for word in line:
            if word == ",":
                text = text + ";\n"
                break
            else:
                text = text + word
        num = num + 1
    else:
        if line.strip() == 'end':
            end = True

# Adds a public rule that allows access to every other rule created before.  When every rule is added, the grammar is written to the file grammar.jsgf.
text = text + "public <command> = "
for x in range(0, num):
    if x == (num - 1):
        text = text + "<%d>;"%x
        f = open("grammar.jsgf","w")
        f.write(text)
        f.close()
    else:
        text = text + "<%d> | "%x

# Runs the executable that converts grammar.jsgf to grammar.fsg
args = ('sphinx_jsgf2fsg', "-jsgf", "grammar.jsgf", "-fsg", "grammar.fsg")
subprocess.Popen(args, stdout=subprocess.PIPE)

old = open("grammar.word", "r")
old_word = old.readlines()
old.close()

# Runs the Perl script that converts grammar.fsg to .word format, then writes to grammar.word
with open("grammar.word", "w") as outfile:
	subprocess.Popen(["perl", "fsg2wlist.pl", "grammar.fsg"], stdout=outfile)

new = open("grammar.word", "r")
new_word = new.readlines()
new.close()

if(new_word != old_word):
        # Runs the script that gets the dictionary
        subprocess.Popen(["python", "get_dict.py"])
