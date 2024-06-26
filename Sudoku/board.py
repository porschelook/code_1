import copy


class board:
    
    def __init__(self):
        self.rule = 1
        self.cells = [
            [{1, 2, 3, 4, 5, 6, 7, 8, 9} for col in range(9)] for row in range(9)
        ]
        self.emptyCells = [(row, col) for col in range(9) for row in range(9)]
        # self.cells = [[{0} for col in range(9)] for row in range(9)]

    def fillCell(self, row, col, value):
        if value not in self.cells[row][col]:
            #print("Attempt at invalid move of value "+ str(value))
            return -1 # decide how to handle this case later
     

        # eliminate the value from other applicable cells

        # eliminate from each element in same row
        for itercol in range(9):
            self.cells[row][itercol].discard(value)

        # eliminate from each element in same column
        for iterrow in range(9):
            self.cells[iterrow][col].discard(value)

        # eliminate the value from each element in the box
        rowoffset = row // 3
        coloffset = col // 3
        for rowiter in range(3):
            for coliter in range(3):
                self.cells[rowoffset * 3 + rowiter][coloffset * 3 + coliter].discard(
                    value
                )

        self.cells[row][col] = {
            value
        }  # make the assignment last, so it can be removed earlier just fine

        try:
            self.emptyCells.remove((row, col))
        except:
            print("already assigned this element")
            return -2

    # Do a forward error check and see if any cell has no valid values, False means that the current board is inconsistent
    def forwardCheck(self):
        for row in range(len(self.cells)):
            for col in range(len(self.cells[0])):
                value=self.cells[row][col]
                if len(value)==0:
                    #print("forward check fails for cell "+ str(row) + "," +str(col))
                    return False
        return True

    # build the starting conditions from the textfile examples. Will require copy-pasting in some way to manage the fact that lots of them are in the same file. This takes in the name of a file to read in, and expects the file to just contain the board it is to build
    def buildBoard(self, instring):
        f = open(instring)
        numFilled = 0
        for i in range(9):
            row = f.readline().replace(" ", "")
            for j in range(9):
                value = int(row[j])
                if value == 0:
                    continue
                # print("placing value " +str(value))
                self.fillCell(i, j, value)
                numFilled += 1
        return numFilled
    def buildBoardString(self,instring):
        numFilled=0
        stringIndex=0
        for i in range(9):
            for j in range(9):
                value=int(instring[stringIndex])
                stringIndex+=1
                if value==0:
                    continue
                #print("placing value " +str(value))
                self.fillCell(i,j,value)
                numFilled+=1
        return numFilled

    def printBoard(self):
        print("-------------------------------------")
        for row in range(9):
            if row % 3 == 0 and row != 0:
                print("-" * 21)
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    print("|", end=" ")
                value = self.cells[row][col]
                if len(value) == 1:
                    print(list(value)[0], end=" ")
                else:
                    print(".", end=" ")
            print()
        print("-------------------------------------")

    def copy(self):
        output = board()
        output.cells = copy.deepcopy(self.cells)

        output.emptyCells = copy.deepcopy(self.emptyCells)
        return output

    def mostConstrainedVariable(self):
        if len(self.emptyCells) == 0:
            print("stopping")
            return 1, 1
        min_domain_size = float("inf")
        for cell in self.emptyCells:
            cell_row, cell_col = cell
            domain_size = len(self.cells[cell_row][cell_col])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                row, col = cell
        return row, col

    def doNakedSingles(self):  # yes I see the unfortunate wording
        # iterate through "empty" cells looking for those who have only one possible action left, then fill those in with the fill cell
        numberOfHits = 0
        for row, col in self.emptyCells:
            values = self.cells[row][col]
            if len(values) == 1:
                self.fillCell(row, col, list(values)[0])
                numberOfHits += 1
        return numberOfHits

    def doHiddenSingles(self):
        # iterate through "empty" cells looking for those who have unique actions
        numberOfHits = 0
        for row, col in self.emptyCells:
            values = self.cells[row][col]

            # remove values present in the row
            for colIter in range(9):
                if colIter == col:
                    continue
                removeVals = self.cells[row][colIter]
                # actually do the removing
                for v in removeVals:
                    values.discard(v)

            # remove values present in the col
            for rowIter in range(9):
                if rowIter == row:
                    continue
                removeVals = self.cells[rowIter][col]
                # actually do the removing
                for v in removeVals:
                    values.discard(v)
            # remove from the box
            rowoffset = row // 3
            coloffset = col // 3
            for rowiter in range(3):
                for coliter in range(3):
                    rowtemp = rowoffset * 3 + rowiter
                    coltemp = coloffset * 3 + coliter
                    if rowtemp == row and coltemp == col:
                        continue

                    removeVals = self.cells[rowtemp][coltemp]
                    for v in removeVals:
                        values.discard(v)
            if len(values) == 1:
                numberOfHits += 1
                self.fillCell(row, col, list(values)[0])
        return numberOfHits

    def doNakedPairs(self):
        # Iterate through "empty" cells looking for naked pairs
        numberOfHits = 0
        for row, col in self.emptyCells:
            
            values = self.cells[row][col]
            #print("values ",values)
            # Check if the cell has exactly two possible values
            if len(values) == 2:
                # Iterate through other cells in the same row
                for other_col in range(9):
                    if other_col != col and values == self.cells[row][other_col]:
                        # Found a naked pair, eliminate these values from other cells in the same row
                        numberOfHits+=1
                        for c in range(9):
                            if c != col and c != other_col:
                                self.cells[row][c] -= values
                                #this code is the same as naked singles
                                '''
                                if len(self.cells[row][c]) == 1:
                                    self.fillCell(row, c, list(self.cells[row][c])[0])
                                    numberOfHits += 1
                                    self.propagateConstraints()'''
                                
                # Iterate through other cells in the same column
                for other_row in range(9):
                    if other_row != row and values == self.cells[other_row][col]:
                        # Found a naked pair, eliminate these values from other cells in the same column
                        numberOfHits+=1
                        for r in range(9):
                            if r != row and r != other_row:
                                self.cells[r][col] -= values
                                '''if len(self.cells[r][col]) == 1:
                                    self.fillCell(r, col, list(self.cells[r][col])[0])
                                    numberOfHits += 1
                                    self.propagateConstraints()'''
                #what about the three by three cell? 

        return numberOfHits

    def doHiddenPairs(self):
        numberOfHits = 0
        for row in range(9):
            for col in range(9):
                values = self.cells[row][col]
                if len(values) > 1:
                    # Check other cells in the same row for hidden pairs
                    for other_col in range(9):
                        if (other_col != col and len(values.intersection(self.cells[row][other_col])) == 2):
                            hidden_pair_values = values.intersection(self.cells[row][other_col])
                            # Found a hidden pair, eliminate other values from these two cells in the same row
                            for c in range(9):
                                if ( c != col and c != other_col and not self.cells[row][c].issubset(hidden_pair_values )):
                                    self.cells[row][c] -= hidden_pair_values
                                    if len(self.cells[row][c]) == 1:
                                        self.fillCell(row, c, list(self.cells[row][c])[0])
                                        numberOfHits += 1
                                        self.propagateConstraints()

                    # Check other cells in the same column for hidden pairs
                    for other_row in range(9):
                        if (other_row != row and len(values.intersection(self.cells[other_row][col]))== 2):
                            hidden_pair_values = values.intersection(self.cells[other_row][col] )
                            # Found a hidden pair, eliminate other values from these two cells in the same column
                            for r in range(9):
                                if ( r != row and r != other_row and not self.cells[r][col].issubset( hidden_pair_values )):
                                    self.cells[r][col] -= hidden_pair_values
                                    if len(self.cells[r][col]) == 1:
                                        self.fillCell(r, col, list(self.cells[r][col])[0] )
                                        numberOfHits += 1
                                        self.propagateConstraints()

        return numberOfHits
    def doNakedTriples(self):
        numberOfHits = 0
        for row in range(9):
            for col in range(9):
                values = self.cells[row][col]
                if len(values) > 1:
                    # Check other cells in the same row for naked triples
                    for other_col1 in range(col + 1, 9):
                        for other_col2 in range(other_col1 + 1, 9):
                            triple_values = values.union(self.cells[row][other_col1], self.cells[row][other_col2])
                            if len(triple_values) == 3:
                                # Found a naked triple, eliminate other values from these three cells in the same row
                                for c in range(9):
                                    if c != col and c != other_col1 and c != other_col2:
                                        self.cells[row][c] -= triple_values
                                        if len(self.cells[row][c]) == 1:
                                            self.fillCell(row, c, list(self.cells[row][c])[0])
                                            numberOfHits += 1
                                            self.propagateConstraints()

                    # Check other cells in the same column for naked triples
                    for other_row1 in range(row + 1, 9):
                        for other_row2 in range(other_row1 + 1, 9):
                            triple_values = values.union(self.cells[other_row1][col], self.cells[other_row2][col])
                            if len(triple_values) == 3:
                                # Found a naked triple, eliminate other values from these three cells in the same column
                                for r in range(9):
                                    if r != row and r != other_row1 and r != other_row2:
                                        self.cells[r][col] -= triple_values
                                        if len(self.cells[r][col]) == 1:
                                            self.fillCell(r, col, list(self.cells[r][col])[0])
                                            numberOfHits += 1
                                            self.propagateConstraints()

        return numberOfHits
    def doHiddenTriples(self):
        numberOfHits = 0
        for row in range(9):
            for col in range(9):
                values = self.cells[row][col]
                if len(values) > 1:
                    # Check other cells in the same row for hidden triples
                    for other_col1 in range(col + 1, 9):
                        for other_col2 in range(other_col1 + 1, 9):
                            triple_values = values.union(self.cells[row][other_col1], self.cells[row][other_col2])
                            if len(triple_values) == 3:
                                # Found a potential hidden triple, check if other cells in the row contain these values
                                hidden_triple_found = True
                                for c in range(9):
                                    if c != col and c != other_col1 and c != other_col2:
                                        if self.cells[row][c].issubset(triple_values):
                                            hidden_triple_found = False
                                            break
                                if hidden_triple_found:
                                    # Found a hidden triple, eliminate other values from these three cells in the same row
                                    for c in range(9):
                                        if c != col and c != other_col1 and c != other_col2:
                                            self.cells[row][c] -= triple_values
                                            if len(self.cells[row][c]) == 1:
                                                self.fillCell(row, c, list(self.cells[row][c])[0])
                                                numberOfHits += 1
                                                self.propagateConstraints()

                    # Check other cells in the same column for hidden triples
                    for other_row1 in range(row + 1, 9):
                        for other_row2 in range(other_row1 + 1, 9):
                            triple_values = values.union(self.cells[other_row1][col], self.cells[other_row2][col])
                            if len(triple_values) == 3:
                                # Found a potential hidden triple, check if other cells in the column contain these values
                                hidden_triple_found = True
                                for r in range(9):
                                    if r != row and r != other_row1 and r != other_row2:
                                        if self.cells[r][col].issubset(triple_values):
                                            hidden_triple_found = False
                                            break
                                if hidden_triple_found:
                                    # Found a hidden triple, eliminate other values from these three cells in the same column
                                    for r in range(9):
                                        if r != row and r != other_row1 and r != other_row2:
                                            self.cells[r][col] -= triple_values
                                            if len(self.cells[r][col]) == 1:
                                                self.fillCell(r, col, list(self.cells[r][col])[0])
                                                numberOfHits += 1
                                                self.propagateConstraints()

        return numberOfHits
 
 

    def propagateConstraints(self):
        return
        while True:
            #default
            hits = self.doNakedSingles()
            if hits > 0:
                continue
            hits = self.doHiddenSingles()
            if hits > 0:
                continue

            if self.rule == 2 or self.rule == 3:
                hits = self.doNakedPairs()
                if hits > 0:
                    continue
                hits = self.doHiddenPairs()
                if hits > 0:
                    continue
                
            if self.rule == 3:
                hits = self.doNakedTriples()
                if hits > 0:
                    continue
                hits = self.doHiddenTriples()
                if hits > 0:
                    continue
            
            break  # If no rule applies, exit the loop

# if __name__ == "__main__":
#     my_board = board()
#     print("forwardCheck ", my_board.forwardCheck())
#     my_board.buildBoard("testExample.txt")
#     my_board.printBoard()
#     # Fill your board with initial values (using buildBoard method)
#     # Then initiate the backtracking search from the first empty cell
#     solution_found = my_board.backtrackSearch()
#     if solution_found:
#         print("Solution found:")
#         my_board.printBoard()
#     else:
#         print("No solution found.")
