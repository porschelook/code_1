import sys
import random
from environment import *
from simpleAgent import *
from RandomAgent import *
from lowmemoryAgent import *
from threeBitAgent import *
from NewAgent import *
import matplotlib.pyplot as plt
import numpy as np

NO_WALL = 0
WALL = 1

vacuum_model = None
sizeofborad = int(input("Select size of borad (type '0' is default)\n"))

model = int(input("Select Model: \n1 Simple_Agent \n2 Random_Agent \n3 ThreeBit_Agent \n4 NewAgent\n"))
numRuns=1
match model:
    case 1:
        print("model_1")
        #set the model to run to be the memoryless deterministic agent
        vacuum_model=SimpleAgent()
        numRuns=1
    case 2:
        print("model_2")
        vacuum_model=RandomAgent()
        numRuns=50
        #set the model to be a random memoryless agent
    case 3:
        print("model_3")
        vacuum_model=threeBitAgent()
        numRuns=1
        #set the model to be a small-memory agent
    case 4:
        print("model_4")
        vacuum_model=NewAgent()
        numRuns=1
        #set the model to be the newwwwwwwwww one

map = int(input("NoWall 1 \nWall 2\n"))

#run a fixed number of steps. 500 should be good

cleanTrace=np.zeros(500)
timetoStop=np.zeros(numRuns)        
for run in range(numRuns):
    #restart the enviornment after each run
    if map == 1:
        state = environment(NO_WALL,sizeofborad)

        state.printCurrentWorld()

 
    if map == 2:
        state = environment(WALL,sizeofborad)
        state.printCurrentWorld()
 

    stop = int(state.ROOM_DIMENSION*state.ROOM_DIMENSION*0.90)
    for i in range(500):
        print(state.clean)
        cleanTrace[i]+=state.clean
        if state.clean >= stop:
            timetoStop[run]=i
        state.printCurrentWorld()
        vacuum_model.stepProgram(state)
    #record relavent parameters for the report

    #state.printCurrentWorld()
cleanTrace/=numRuns 
plt.plot(cleanTrace)
plt.xlabel("Number of steps")
plt.ylabel("Average number of clean tiles")
plt.show()
