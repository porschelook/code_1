from environment import *
class Agent:
    def stepProgram(self,environment):
        return


class SimpleAgent(Agent):
    def stepProgram(self,environment):

        #first, if the room is dirty, clean it
        if(not environment.getCurrentRoom().Isclean):
            environment.getCurrentRoom().Isclean=True
            return
        #Next, if the way forward is clear, move forward
        if(not environment.detectWall()):
            environment.advance()
            return
        #If the way is blocked, turn right
        environment.turnRight()
    