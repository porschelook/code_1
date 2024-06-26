from environment import *
from simpleAgent import *
import itertools
import copy

Up, Down, Left, Right= range(4)

class BeliefNode:
    def __init__(self,env=None):
        if env==None:
            
            
            #for now there are no walls NEXT STEP is EXTRACT WALS
            self.beliefCells=[]
            self.current_x=0
            self.current_y=0
            self.currentFacing=Up
            #for now, use fixed size
            self.scanDistance=2
            self.height=0
            self.width=0
            #need to run an and-or plan
            return
        
        #extract list of walls, build new architecture that captures belief states.
        #fill in walls with the symbol w
        #for now there are no walls
        self.beliefCells=[[{0,1} for cell in row] for row in env.rooms]
        self.current_x=env.current_x
        self.current_y=env.current_y
        self.currentFacing=Up
        self.height=len(self.beliefCells)
        self.width=len(self.beliefCells[1])
        self.scanDistance=env.scanDistance
    #return a deep copy
    def copy(self):
        out=BeliefNode()
        out.beliefCells=copy.deepcopy(self.beliefCells)
        out.current_x=self.current_x
        out.current_y=self.current_y
        out.currentFacing= self.currentFacing
        out.scanDistance=self.scanDistance
        out.height=len(self.beliefCells)
        out.width=len(self.beliefCells[1])
        return out
    def __hash__(self):
        has="("+str(self.current_x)+","+str(self.current_y)+","+str(self.currentFacing)+");\n"
        for row in self.beliefCells:
            
            for item in row:
                if item=={1,0}:
                    has+="?"
                else:
                    has+=str(item)
            has+="\n"

        return hash(has)
    def __eq__(self,other):
        return self.__hash__()==other.__hash__()
   
               
    #This will return a set of states based on all posibilities of the scanning operation
    def scan(self):
        out=[]
        if self.currentFacing==Up:
            selectx=self.current_x
            starty=self.current_y
            endy=max(0,self.current_y-self.scanDistance)
            perms=itertools.product([0,1],repeat=abs(starty-endy))
            for item in perms:
                additionalElement=self.copy()
                j=0
                for y in range(starty,endy, -1):
                    #print(item[j])
                    #print(additionalElement.beliefCells[y][selectx])
                    if (additionalElement.beliefCells[y][selectx])=={1,0}:
                        additionalElement.beliefCells[y][selectx]=item[j]
                        
                    j+=1
                out.append(additionalElement)
            return out
        
        if self.currentFacing==Down:
            selectx=self.current_x
            starty=self.current_y
            endy=min(self.height,self.current_y+self.scanDistance)
            perms=itertools.product([0,1],repeat=abs(starty-endy))
            for item in perms:
                additionalElement=self.copy()
                j=0
                for y in range(starty,endy, 1):
                    if (additionalElement.beliefCells[y][selectx])=={1,0}:
                        additionalElement.beliefCells[y][selectx]=item[j]
                    j+=1
                out.append(additionalElement)
            return out
        
        if self.currentFacing==Left:
            selecty=self.current_y
            startx=self.current_x
            endx=max(0,self.current_x-self.scanDistance)
            perms=itertools.product([0,1],repeat=abs(startx-endx))
            for item in perms:
                additionalElement=self.copy()
                j=0
                for x in range(startx,endx, -1):
                    if (additionalElement.beliefCells[selecty][x])=={1,0}:
                        additionalElement.beliefCells[selecty][x]=item[j]
                    j+=1
                out.append(additionalElement)
            return out
        
        if self.currentFacing==Right:
            selecty=self.current_y
            startx=self.current_x
            endx=min(self.width,self.current_x+self.scanDistance)
            perms=itertools.product([0,1],repeat=abs(startx-endx))
            for item in perms:
                additionalElement=self.copy()
                j=0
                for x in range(startx,endx, 1):
                    if (additionalElement.beliefCells[selecty][x])=={1,0}:
                        additionalElement.beliefCells[selecty][x]=item[j]
                    j+=1
                out.append(additionalElement)
            return out
        #define all the actions, turning and advancing (which automatically scans), and cleaning
    def isGoal(self):
        for row in self.beliefCells:
                    
            for item in row:
                if item!=0:
                    return False
        return True
    def clean(self):
        out=self.copy()
        out.beliefCells[self.current_y][self.current_x]=0
        return out
    def advance(self):
        # moves based on stored orientation
        result=self.copy()
        if self.currentFacing == Up:
            result.current_y -= 1
        if self.currentFacing == Down:
            result.current_y += 1
        if self.currentFacing == Right:
            result.current_x += 1
        if self.currentFacing == Left:
            result.current_x -= 1
        # fix position to be within bounds
        if result.current_y < 0:
            return None
        
        if result.current_x <0:
            return None
        if result.current_y >=self.height:
            return None
        if result.current_x >= self.width:
            return None
        # Next is to fix the robot from encountering a wall in the middle of the field
        if result.beliefCells[result.current_y][result.current_x]=="w":
            return None#don't go into a wall

        return result.scan()
    
    def turnLeft(self):
        result=self.copy()
        result.currentFacing=(result.currentFacing-1)%4
        return result.scan()
    def turnRight(self):
        result=self.copy()
        result.currentFacing=(result.currentFacing+1)%4
        return result.scan()
    def currentCellDirty(self):
        return self.beliefCells[self.current_y][self.current_x]==1
class NewAgent(Agent):
    def __init__(self, env):# needs to generate the plan before it executes it
        self.beliefSpace=BeliefNode(env)
        self.plan=self.AndOrSearch()
        print(self.plan)
        
    #it is valid in this case to have a map from belief states to actions because repeated belief states will never occur.  In other words, detect cycles by returning to the same belief state
    def AndOrSearch(self):
        #this uses iterative deepening
        #start with and search instead because the first action will be scan
        plan={self.beliefSpace:"scan"}
        lim=1
        plan=self.AndSearch(self.beliefSpace.scan(),plan,set(),lim)
        while plan is None:
            lim+=1
            plan={self.beliefSpace:"scan"}
            plan=self.AndSearch(self.beliefSpace.scan(),plan,set(),lim)
        print(lim)
        return plan
    def AndSearch(self,states,plan,path,depthlim):
        if depthlim<0:
            return None#went too deep
        output={}#new dictionary
        #print(states)
        if states is None:#this detects wall collisions
            return None
        for state in states:
            partialPlan=self.OrSearch(state,plan,path,depthlim-1)
            if partialPlan is None:
                return None
            output.update(partialPlan)#append plan together
        return output
    def OrSearch(self,state,plan,path,depthlim):
        if state in path:
            return None
        
        #check for goal state
        if state.isGoal():
            output= copy.deepcopy(plan)
            output[state]="stop"#append to the plan
            output["goal"]=True
            return output
        if state in plan.keys():
            return None#this is to mark a failure
        newPath=copy.deepcopy(path)
        newPath.add(state)
        #try each action, but only if it is useful
        if state.currentCellDirty():
            
            NewPlan = self.AndSearch([state.clean()],plan,newPath,depthlim)
            if NewPlan is not None:
                output= copy.deepcopy(NewPlan)
                output[state]="clean"#append to the plan
                return output
        #try advancing, if it would reach a wall that will be detected elsewhere
        NewPlan = self.AndSearch(state.advance(),plan,newPath,depthlim)
        if NewPlan is not None:
            output= copy.deepcopy(NewPlan)
            output[state]="advance"#append to the plan
            return output
        #try turning right
        NewPlan = self.AndSearch(state.turnRight(),plan,newPath,depthlim)
        if NewPlan is not None:
            output= copy.deepcopy(NewPlan)
            output[state]="right"#append to the plan
            return output
        #left
        NewPlan = self.AndSearch(state.turnLeft(),plan,newPath,depthlim)
        if NewPlan is not None:
            output= copy.deepcopy(NewPlan)
            output[state]="left"#append to the plan
            return output
        return None
    def fillScan(self,scanResults):
        direction=self.beliefSpace.currentFacing
        i=0
        for item in scanResults:
            if item.Isclean:
                cell=0
            else:
                cell=1
            #This needs to include whether it is a wall, which still isn't quite clear to me. 
            #if item.isWall:
             #   cell="w"
            
            if direction==Down:
                self.beliefSpace.beliefCells[self.beliefSpace.current_y-i][self.beliefSpace.current_x]=cell
            if direction==Up:
                self.beliefSpace.beliefCells[self.beliefSpace.current_y+i][self.beliefSpace.current_x]=cell
            if direction==Left:
                self.beliefSpace.beliefCells[self.beliefSpace.current_y][self.beliefSpace.current_x-i]=cell
            if direction==Right:
                self.beliefSpace.beliefCells[self.beliefSpace.current_y][self.beliefSpace.current_x+i]=cell
            i+=1
    def stepProgram(self,environment):
        # from simple agent **********************************************************
        outputs=environment.scan()
        self.fillScan(outputs)
        move=self.plan[self.beliefSpace]
        print(move)
        if move=="advance":
            environment.advance()
        if move=="left":
            environment.turnLeft()
        if move=="right":
            environment.turnRight()
        if move=="clean":
           self.clean(environment)
