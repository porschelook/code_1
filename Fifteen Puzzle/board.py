import numpy as np
import random

GOAL = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
class state:
    
    def __init__(self, board=None):
        #init into the solved state
        if board is None:
            temp=np.arange(15)+1#fifteen for the fifteen puzzle.
            temp=np.concatenate((temp,np.array([0])))#add in a zero for the empty cell
            self.board=np.reshape(temp,(4,4))# this is in row-major order so the first index is which row it is in and the second is which coilumn it is in.
             
        else:
            self.board=board.copy()#does a deep copy
            
        self.emptyLoc=(3,3)#initialize the spot of the empty square so it doesn't need to be searched for
        self.row=4
        self.col=4

    def scramble(self,numSteps):
        lastMove=None
        moves={"up", "right","left","down"}
        for i in range(numSteps):
            move=random.choice(tuple(moves-{lastMove}))
            #randomly choose a step that isn't the last one
            lastMove=move
            #apply move
            if move=="up":
                self.moveUp()
            if move=="right":
                self.moveRight()
            if move=="left":
                self.moveLeft()
            if move=="down":
                self.moveDown()    
    #changes the board state to that for which the empty (0) square has moved up one tile.         
    def moveUp(self):
        assert self.board[self.emptyLoc]==0
        newEmptyLoc=( max(0,self.emptyLoc[1]-1),self.emptyLoc[0])
        self.board[newEmptyLoc], self.board[self.emptyLoc]=self.board[self.emptyLoc], self.board[newEmptyLoc]
        self.emptyLoc=newEmptyLoc

    def moveDown(self):
        assert self.board[self.emptyLoc]==0
        newEmptyLoc=( min(3,self.emptyLoc[1]+1),self.emptyLoc[0])
        self.board[newEmptyLoc], self.board[self.emptyLoc]=self.board[self.emptyLoc], self.board[newEmptyLoc]
        self.emptyLoc=newEmptyLoc


    def moveLeft(self):
        assert self.board[self.emptyLoc]==0
        newEmptyLoc=(self.emptyLoc[0], max(0,self.emptyLoc[1]-1))
        self.board[newEmptyLoc], self.board[self.emptyLoc]=self.board[self.emptyLoc], self.board[newEmptyLoc]
        self.emptyLoc=newEmptyLoc

    def moveRight(self):
        assert self.board[self.emptyLoc]==0
        newEmptyLoc=(self.emptyLoc[0], min(3,self.emptyLoc[1]+1))
        self.board[newEmptyLoc], self.board[self.emptyLoc]=self.board[self.emptyLoc], self.board[newEmptyLoc]
        self.emptyLoc=newEmptyLoc

    def print_current_board(self):

        for i in self.board:
            for j in i:
                print(j, " ", end="")
            print()

    def copy(self):
        return state(board=self.board)


    def manh_dist(self):
        dist = 0
        for row in range(self.row):
            for col in range(self.col):
                if (value := self.board[row][col]) != 0:
                    print("v ",value)
                    value -= 1
                    x = value % self.col
                    y = value // self.row
                    dist += abs(x - col) + abs(y - row)
                    print("dist ",dist)
        return dist
    
    def is_goal(self):
        if self.manh_dist() == 0:
            return True
        return False

class Node:
    def __init__(self, state, cost, heuristic, parent=None):
        self.state = state
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent
        self.f_score = cost + heuristic

def aStar(self):
    open_list = [Node(self, 0, self.manh_dist())]  # Start with the initial state
    closed_list = []

    while open_list:
        current_node = min(open_list, key=lambda x: x.f_score)
        open_list.remove(current_node)
        closed_list.append(current_node)

        if current_node.state.is_goal():  # Define a method is_goal() to check if the state is the goal state
            return current_node  # Return the goal node

        # Generate successor states and add them to the open list
        for move in ["up", "down", "left", "right"]:
            successor_state = current_node.state.copy()
            getattr(successor_state, f"move{move.capitalize()}")()  # Perform the move
            cost = current_node.cost + 1  # Assume uniform cost for each move
            heuristic = successor_state.manh_dist()
            successor_node = Node(successor_state, cost, heuristic, current_node)
            if successor_node not in closed_list:
                open_list.append(successor_node)

    return None  # No solution found