#!/usr/bin/python
import re
import itertools
from itertools import compress, count, imap, islice
from functools import partial
from operator import eq
import copy

arr1 = []
arr2 = []
max = 0
max_elements = []
source = ""
target = ""

# CHANGE THESE IF ON A NEW MACHINE/FILES ARE MOVED
fw = open("2nd_demo.graphml","w")
fr = open("readfrom_2.txt","r")
lines = fr.readlines()
fr.close()

text = """<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
        http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
    <key id="d0" for="node" attr.name="dialogue" attr.type="string"/>
    <key id="d1" for="edge" attr.name="spoken" attr.type="string"/>
    <graph id="G" edgedefault="directed">"""
fw.write(text+'\n')

# Splits all words separated by | into seperate strings and puts them in an array
def split_string_or(A):
    if A.count('|')>=0:
        orNum = A.count('|')
        tempNum=0
        arr = []
        while tempNum<=orNum:
            orText = A.split('|')[tempNum]
            orTextNew = clean_string(orText)
            tempNum=tempNum+1
            arr.append(orTextNew)
    return arr

# remove unwanted characters from strings
def clean_string(St):
    StNew = St.strip("[], (), |")
    StNew = StNew.replace("[","")
    StNew = StNew.replace("]","")
    StNew = StNew.replace("(","")
    StNew = StNew.replace(")","")
    StNew = StNew.replace("|","")
    return StNew

# Splits the string from the line into necessary words in arr1 and unnecessary words in arr2
def split(S, count1, count2):
    global arr1
    global arr2
    
    # if there are no more sets of parentheses
    if count1 == (S.count('(')):
        # if there are no more sets of brackets
        if count2 == (S.count('[')):
            # add the number of bracketed or parenthesized phrases to the end of the lists
            arr1.append(count1)
            arr2.append(count2)
        # if there are more brackets
        else:
            ok=S.split(']')[count2]
            ok2=ok.split('[')[1]
            arr2+=(split_string_or(ok2))
            arr2.append('split')
            arr1.append('*') # '*' marks where an optional word will be inserted
            split(S, count1, count2 + 1)
    else:
        if count2 == (S.count('[')):
            ok=S.split(')')[count1]
            ok2=ok.split('(')[1]
            arr1+=(split_string_or(ok2))
            arr1.append('split')
            split(S, count1 + 1, count2)
        else:
            ok=S.split(')')[count1]
            ok2=ok.split('(')[1]
            ok3=S.split(']')[count2]
            ok4=ok3.split('[')[1]
            if(S.find(ok2) < S.find(ok4)):
                arr1+=(split_string_or(ok2))
                arr1.append('split')
                split(S, count1 + 1, count2)
            else:
                arr3 = []
                arr3 += split_string_or(ok4)
                arr2+=arr3
                arr2.append('split')
                arr1.append('*')
                split(S, count1, count2 + 1)

# Finds the nth instance of a symbol in an array
def nth_item(n, item, iterable):
    indicies = compress(count(), imap(partial(eq, item), iterable))
    return next(islice(indicies, n, None), -1)

# starts recursion with optional strings
def insert(arr):
    global max_elements
    global max
    max = arr[-1]     # The last val in arr holds the number of elements
    max_elements = [None] * max # new array with max num of vals
    max_elements = position(arr, max_elements)
    cry = copy.copy(max_elements)
    loop2(cry, [])

# gets the array of current choices for the combinations
def get_elts(yup, option, option2): #<- current, arr2, max_elts
    arr = []
    arr.append([option[yup[0]], 0])
    if len(yup) > 1:
        add = option2[0] + 2
        for x in range(1, len(yup)):
            arr.append([option[yup[x] + add], x])
            add = add + option2[x] + 2
    return arr

# figures out how many words are in each set of options
# one set of options could be ( a | b | c ) or [a | b | c]
def position(arr, answer):
    sub = 0;
    for x in range(0, len(answer)):
        val = nth_item(x, 'split', arr)
        answer[x] = val - (sub + 1)
        sub += (val+1 - sub)
    return answer

# Finds every possible combination of optional words, inserts each of these into the necessary words array, and sends that array
# to be broken into every possible combination of necessary words.
def loop2(current_elements, past_elements):
    chained = get_elts(current_elements, arr2, max_elements)
    for x in range(1, max+1):
        for combination in itertools.combinations(chained, x):
            temp = copy.copy(arr1)
            repeat = 0;
            for element in combination:
                index = nth_item(chained.index(element), '*', temp)
                temp.insert(index, element[0])
                temp.insert(index+1, 'split')
                temp[len(temp)-1]+=1
            for j in range(0, len(past_elements)):
                if x == 1:
                    if list(combination)[0] in past_elements[j]:
                        repeat += 1
                else:
                    if list(combination) in past_elements:
                        repeat += 1
            if repeat < 1:
                temp[:] = [y for y in temp if y != '*']
                necessary_words(temp)
    if all([ v == 0 for v in current_elements ]):
        return;
    else:
        next_combo(current_elements, len(current_elements)-1, max_elements)
        past_elements.append(chained)
        loop2(current_elements, past_elements)

# changes values in current_elements
# if the value in the place in the array is at 0, look at the next place to the left.
# if the value is not zero, subtract one, then reset any values to the right of this digit to their original values
# eg if the max values are 1 2 5 6, 1 2 5 0 -> 1 2 4 6
def next_combo(vals, current, reset):
    if vals[current] != 0:
        vals[current] -= 1
        if len(vals)-1 > current:
            for y in range((current+1), len(vals)):
                vals[y] = reset[y]
    else:
        next_combo(vals, current-1, reset)

# Setup for finding all combinations with n words, where n is the number of groups of options
def necessary_words(array):
    num_elts = array[-1]     # The last val in arr holds the number of elements
    necessary_elements = [None] * num_elts # new array with num of vals
    position(array, necessary_elements)
    current_elts = copy.copy(necessary_elements)# starting current elements are the same as the maximum
    generate_combos(current_elts, array, necessary_elements)

# Finds all combinations with n words, where n is the number of groups of options
def generate_combos(current, array, maximum):
    chained = get_elts(current, array, maximum)
    full_string = ""
    for x in range(0, len(chained)):
        full_string += chained[x][0]
        full_string += " "
    print 'FINAL'
    print full_string
    fw.write('\n'+ '<edge source="' + str(source) + '" target="' + str(target) + '">' + '<data key="d1">'+ full_string.rstrip()+ '</data></edge>')
    
    if all([ v == 0 for v in current]):
        return;
    else:
        next_combo(current, len(current)-1, maximum)
        generate_combos(current, array, maximum)


end = False
for line in lines:
    if end == False:
        if line.rstrip() == 'end':
            end = True
        else:
            #get the string before = (the name of the node)
            nodeID = line.partition('=')[0].rstrip().lstrip()
            #get the string after = (the data stored in the node)
            nodeData = line.rpartition("=")[2].rstrip().lstrip()
            #format the text like in .graphml
            nodeText = '\n'+'<node id="' + str(nodeID) + '">' + '<data key="d0">'+nodeData+"</data>"+"</node>"
            fw.write(nodeText)
    else:
        if line.rstrip() != "":
            # reset values
            arr1 = []
            arr2 = []
            max = 0
            max_elements = []
            source = ""
            target = ""
            
            # get the edge data, the node the edge comes from, and the node the edge goes to
            # rstrip() and lstrip() remove spaces on either side of the text.
            edgeData = line.partition(',')[0]
            step = line.partition(',')[2]
            source = step.partition(',')[0].rstrip().lstrip()
            target = line.rpartition(",")[2].rstrip().lstrip()
            
            # put all the parenthesized words in arr1 and all the bracketed words in arr2
            split(edgeData, 0, 0)

            hi = copy.copy(arr1)
            hi[:] = [y for y in hi if y != '*']
            if len(hi) > 1:
                # find the possible phrases without optional words
                necessary_words(hi)
            if len(arr2) > 1:
                # find the possible phrases with optional words
                insert(arr2)
fw.write('</graph> </graphml>')
fw.close()
