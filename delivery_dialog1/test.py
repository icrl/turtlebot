fw = open("/home/raeesa/networkx/examples/write_graphml.graphml","w")
fr = open("readfrom.txt","r")
lines = fr.readlines()
fr.close()

text = """<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
        http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
    <key id="d0" for="node" attr.name="dialogue" attr.type="string"/>
    <key id="d1" for="edge" attr.name="spoken" attr.type="string"/>
    <graph id="G" edgedefault="directed"><node id="n1"><data key="d0">root</data></node>"""
fw.write(text+'\n')
number = 0
nodeID = 1
for line in lines:
	nodeID = nodeID+1
	
	#get the string after =
	nodeData = line.rpartition("=")[2].rstrip()
	nodeText = '\n'+'<node id="n'+ str(nodeID) + '">' + '<data key="d0">'+nodeData+"</data>"+"</node>"
	#print text
	fw.write(nodeText)
	
	edgeData = line.rpartition("=")[0]

	#check if the string edgeData starts with"("
	#if edgeData[0] == "(":
	part1 = edgeData.rpartition(")")[0]
	part2 = edgeData.rpartition(")")[2]
	part2 = part2[1:]
	part2 = part2[:-1]
	part1 = part1[1:]
	num = part1.count("|")
	#loop until we reach num
	tempNum=0
	while tempNum<=num:
		temp = part1.split("|")[tempNum]
		#print temp
		tempNum = tempNum+1
		#include the second part of the string 'Turtlebot'
		#write it into the file as edges
		edgeText = '\n'+'<edge source="n1" target="n'+str(nodeID)+'">'+'\n'+'<data key="d1">'+temp+'</data>'+'\n'+'</edge>'
		edgeText2 = '\n'+'<edge source="n1" target="n'+str(nodeID)+'">'+'\n'+'<data key="d1">'+temp+' '+part2+'</data>'+'\n'+'</edge>'
		print edgeText
		fw.write(edgeText)
		fw.write(edgeText2)
endText = "</graph></graphml>"
fw.write(endText)
fw.close()
