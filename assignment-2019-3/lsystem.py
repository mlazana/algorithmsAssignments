import json
import sys
import math
import argparse
import string
import re


parser = argparse.ArgumentParser()

parser.add_argument("input_file", help="Insert your json file containing grammar")
parser.add_argument("output_file", nargs="?",
                    help="Specify your output_file name which will contain the coordinates")
parser.add_argument("-m", help="Produces String output", action="store_true")
parser.add_argument("-d", help="Producing the rules of a given image", action="store_true")

args = parser.parse_args()

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

if not args.d:
    with open(args.input_file) as json_file: 
        grammar = json.load(json_file)

        rules = grammar["rules"]
        word = grammar["axiom"]
        
        #Creating string 
        for i in range(grammar["order"]):
            word = list(word)
            for s in range(len(word)):
                if word[s] in rules:
                    word[s] = rules[word[s]]
            word = ''.join(word)
        
if args.m:
    print(word)

'''-------------- Coordinates creation -------------------'''
if not args.m and not args.d :
    output_file = open(args.output_file, "w")
    #Create tuples for the coordinates
    start_coordinates = (0,0)
    #Starting angle
    angle = grammar["start_angle"]
    step = grammar["step_length"]
    #Create stacks for keeping positions
    stack_coordinates = []
    stack_angle = []
    alphabet = str(string.ascii_uppercase)
    for w in word:
        if w == "[" :
            stack_coordinates.append(start_coordinates)
            stack_angle.append(angle)
        elif w == "]" :
            start_coordinates = stack_coordinates.pop()
            angle = stack_angle.pop()
        elif w == "+" :
            angle += grammar["left_angle"]
        elif w == "-" :
            angle -= grammar["right_angle"]
        elif w in alphabet[:len(alphabet)//2] :
            x = (math.cos(math.radians(angle))*step + start_coordinates[0])
            y = (math.sin(math.radians(angle))*step + start_coordinates[1])
            end_coordinates = (round(x,2),round(y,2))
            output_file.write(str(start_coordinates) + ' ' + str(end_coordinates) + '\n')
            start_coordinates = end_coordinates
        
'''-------------- Rules creation ------------------- '''
if args.d: 
    # Third part can print right +/- but not L or R  
    with open(args.input_file) as txt: 

        content = txt.readlines() 
        looking = "r"
        for step in content:
            step = [float(s) for s in re.findall(r'-?\d+\.?\d*', step)]
            #print(step)
            if step[0] != step[2]:
                if step[0] < step[2]:
                    change = "+x"
                else:
                    change = "-x"
            else:
                if step[1] < step[3]:
                    change = "+y"
                else:
                    change = "-y"
            #print(looking, "||", change)
            '''---- for x and y changes ----'''
            if (looking == "r" and change == "+y") :
                print("+")
                looking = "f"
            elif (looking == "l" and change == "-y"):
                print("+")
                looking = "d"
            elif (looking == "r" and change == "-y"):
                print("-")
                looking = "d"
            elif (looking == "l" and change == "+y"):
                print("-")
                looking = "f"
            elif (looking == "f" and change == "+x") :
                print("-")
                looking = "r"
            elif (looking == "f" and change == "-x"):
                print("+")
                looking = "l"
            elif (looking == "d" and change == "-x"):
                print("-")
                looking = "l"
            elif (looking == "d" and change == "+x"):
                print("+")
                looking = "r"
            print("Sorry, third part is under construction!")
            print("My way of dealing with this problem is written in documentation")