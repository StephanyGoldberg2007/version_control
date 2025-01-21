from itertools import count

import numpy as np
import random
import json
import copy

class Game:
    def __init__(self):
        self.board = np.zeros(shape=(5,7),dtype=int) # board of 5 rows and 7 columns
        self.player = -1  # player represents the O/white pieces in the game
        self.agent = 1  # agent represents the X/black pieces in the game

        # general one-game features
        self.legal_empty = self.legalMove() # list of empty places where you can place a legal move
        self.last_move = ((0,0),0) # last place on board where a move was made, who made the move
        self.col_remove_agent = True # True - agent didn't remove a column yet, False - already removed a column
        self.col_remove_player = True # True - player didn't remove a column yet, False - already removed a column

        # features for reinforcement learning
        self.winner = 0  # who won the game
        self.all_game_boards = [] # strings of all the boards during one game
        self.boards_and_grades = [] # list of - 1. string of each board, 2. its grade
        self.grade_agent = 10  # grade of board when agent wins
        self.grade_player = 0  # grade of board when player wins
        self.grade_tie = 1  # grade of boards when there is a tie
        self.gamma = 0.9  # determines the grade of the other boards

        # features for heuristics
        self.player3grade = 100
        self.player2grade = 10
        self.agent3grade = -100
        self.agent2grade = -10

    def legalMove(self):
        # creates a list of all the empty places you can place a move on
        self.legal_empty = []
        for i in range (7):
            # goes over all the columns and adds the bottom cell to the list
            self.legal_empty.append((4,i))
        return self.legal_empty

    def agentTurn(self):
        if self.col_remove_agent: # if the agent didn't remove a column yet
            count = 0 # counts the empty columns
            for col in range (7):
                # goes over the lowest row and checks if it's empty
                if (4,col) in self.legal_empty or self.board[4,col] == -2: # if the column is empty or already removed the count goes up
                    count += 1
            if count == 7: # if all the columns are empty - you can't remove a column
                rnd_choice = 1
            else:
                rnd_choice = random.randint(1,100) # decides to make a move (1-50) or remove a column (51-100)
        else: # the agent already removed a column
            rnd_choice = 1

        if rnd_choice <= 50: # making a move - placing a piece
            rnd_place = random.randint(0, len(self.legal_empty) - 1) # picks a random number that represents the index in the list of legal moves
            place = self.legal_empty[rnd_place]
            self.board[place[0], place[1]] = self.agent # places the piece of the agent on the board in the chosen place
            if place[0] > 0 : # if there is a place above the current cell
                self.legal_empty.append((place[0]-1,place[1])) # adds the place above the current place to list of empty legal places
            self.legal_empty.remove(place) # removes the place from the list of the legal empty places
            self.last_move = place, self.agent # the last move - the  index of the place and the number of the agent

        else: # removing a column
            self.removeColumn()
            self.col_remove_agent = False # changes the feature to "False" to not be able to remove another one
            self.last_move = (5,7), self.agent # the last move - index out of the board range represents the removing of column

    def smartAgent(self):
        max_grade = 0 # saves the highest grade
        count_possible_moves = 0 # counts how many possible options the agent has
        count_non_existent = 0 # counts how many boards aren't in the dictionaries
        place = None

        for option in self.legal_empty: # goes over the cells in the list of empty legal places
            count_possible_moves += 1 # counts the board option
            temp_board = copy.deepcopy(self.board) # copies the current board
            temp_board[option[0],option[1]] = 1 # changes the board in the current empty cell
            string_board, count = self.boardToString(temp_board) # changes the board option to string to access it in the dictionary

            # access the correct board according to the number of pieces on the board
            if 0 < count < 19:
                if string_board in games.my_dict1:
                    # if the board exists in the dictionary
                    temp_grade = games.my_dict1[string_board][0] # the grade of that board in the dictionary
                    if temp_grade > max_grade: # if this grade is higher than the current max
                        max_grade = temp_grade
                        place = option # saves the empty cell
                else: count_non_existent += 1 # the board doesn't exist in the dictionary - the count goes up

            if 18 < count < 22:
                if string_board in games.my_dict2:
                    # if the board exists in the dictionary
                    temp_grade = games.my_dict2[string_board][0] # the grade of that board in the dictionary
                    if temp_grade > max_grade:
                        max_grade = temp_grade
                        place = option # saves the empty cell
                else: # the board doesn't exist in the dictionary - the count goes up
                    count_non_existent += 1

            if 21 < count < 26:
                if string_board in games.my_dict3:
                    # if the board exists in the dictionary
                    temp_grade = games.my_dict3[string_board][0] # the grade of that board in the dictionary
                    if temp_grade > max_grade:
                        max_grade = temp_grade
                        place = option # saves the empty cell
                else: # the board doesn't exist in the dictionary - the count goes up
                    count_non_existent += 1

            if 25 < count < 30:
                if string_board in games.my_dict4:
                    # if the board exists in the dictionary
                    temp_grade = games.my_dict4[string_board][0] # the grade of that board in the dictionary
                    if temp_grade > max_grade:
                        max_grade = temp_grade
                        place = option # saves the empty cell
                else: # the board doesn't exist in the dictionary - the count goes up
                    count_non_existent += 1

            if 29 < count < 36:
                if string_board in games.my_dict5:
                    # if the board exists in the dictionary
                    temp_grade = games.my_dict5[string_board][0] # the grade of that board in the dictionary
                    if temp_grade > max_grade:
                        max_grade = temp_grade
                        place = option # saves the empty cell
                else: # the board doesn't exist in the dictionary - the count goes up
                    count_non_existent += 1

        # if the agent still hasn't removed a column
        if self.col_remove_agent:
            for column in self.legal_empty: # goes over the empty legal places
                if column[0] < 4: # if the empty place is not in the bottom row - this column can be removed
                    temp_board = copy.deepcopy(self.board) # copies the current board
                    count_possible_moves += 1  # counts the board option
                    for i in range(5):  # goes over the chosen column and disables the rows
                        temp_board[i, column[1]] = -2
                    string_board, count = self.boardToString(temp_board)  # changes the board option to string to access it in the dictionary

                    # access the correct board according to the number of pieces on the board
                    if 0 < count < 19:
                        if string_board in games.my_dict1:
                            # if the board exists in the dictionary
                            temp_grade = games.my_dict1[string_board][0]  # the grade of that board in the dictionary
                            if temp_grade > max_grade:  # if this grade is higher than the current max
                                max_grade = temp_grade
                                num_col = column[1]  # saves the possible removed column
                                place = (5, 7)  # the saved place is out of the range of the board - to mark a remove of a column
                        else:  # the board doesn't exist in the dictionary - the count goes up
                            count_non_existent += 1

                    if 18 < count < 22:
                        if string_board in games.my_dict2:
                            # if the board exists in the dictionary
                            temp_grade = games.my_dict2[string_board][0]  # the grade of that board in the dictionary
                            if temp_grade > max_grade:  # if this grade is higher than the current max
                                max_grade = temp_grade
                                num_col = column[1]  # saves the possible removed column
                                place = (5, 7)  # the saved place is out of the range of the board - to mark a remove of a column
                        else:  # the board doesn't exist in the dictionary - the count goes up
                            count_non_existent += 1

                    if 21 < count < 26:
                        if string_board in games.my_dict3:
                            # if the board exists in the dictionary
                            temp_grade = games.my_dict3[string_board][0]  # the grade of that board in the dictionary
                            if temp_grade > max_grade:  # if this grade is higher than the current max
                                max_grade = temp_grade
                                num_col = column[1]  # saves the possible removed column
                                place = (5, 7)  # the saved place is out of the range of the board - to mark a remove of a column
                        else:  # the board doesn't exist in the dictionary - the count goes up
                            count_non_existent += 1

                    if 25 < count < 30:
                        if string_board in games.my_dict4:
                            # if the board exists in the dictionary
                            temp_grade = games.my_dict4[string_board][0]  # the grade of that board in the dictionary
                            if temp_grade > max_grade:  # if this grade is higher than the current max
                                max_grade = temp_grade
                                num_col = column[1]  # saves the possible removed column
                                place = (5, 7)  # the saved place is out of the range of the board - to mark a remove of a column
                        else:  # the board doesn't exist in the dictionary - the count goes up
                            count_non_existent += 1

                    if 29 < count < 36:
                        if string_board in games.my_dict5:
                            # if the board exists in the dictionary
                            temp_grade = games.my_dict5[string_board][0]  # the grade of that board in the dictionary
                            if temp_grade > max_grade:  # if this grade is higher than the current max
                                max_grade = temp_grade
                                num_col = column[1]  # saves the possible removed column
                                place = (5, 7)  # the saved place is out of the range of the board - to mark a remove of a column
                        else:  # the board doesn't exist in the dictionary - the count goes up
                            count_non_existent += 1

        if count_non_existent > (count_possible_moves/2) or place is None:
            # if more than half of the possible moves don't exist in the dictionary, the agent plays randomly
            self.agentTurn()
        else: # there are enough boards in the dictionary
            if place[0] == 5: # if the saved place was (5,7) there is going to be a column removed
                for row in range(5):  # goes over all the rows in the removed column and disables them
                    cell = (row, num_col)  # the current cell
                    self.board[cell[0], cell[1]] = -2  # disabling the cell
                    if cell in self.legal_empty:  # if the cell was empty and legal for a move it's removed from the list
                        self.legal_empty.remove(cell)
                self.col_remove_agent = False  # changes the feature to "False" to not be able to remove another one
                self.last_move = place, self.agent  # the last move - index out of the board range represents the removing of column
            else: # the removed cell is an empty place on the board
                self.board[place[0], place[1]] = self.agent  # places the piece of the agent on the board in the chosen place
                if place[0] > 0:  # if there is a place above the current cell
                    self.legal_empty.append((place[0] - 1, place[1]))  # adds the place above the current place to list of empty legal places
                self.legal_empty.remove(place) # removes the place from the list of the legal empty places
                self.last_move = place, self.agent  # the last move - the  index of the place and the number of the agent

    def playerTurn(self):
        if self.col_remove_player: # if the agent didn't remove a column yet
            count = 0 # counts the empty columns
            for col in range (7):
                # goes over the lowest row and checks if it's empty
                if (4,col) in self.legal_empty or self.board[4,col] == -2: # if the column is empty or already removed the count goes up
                    count += 1
            if count == 7: # if all the columns are empty - you can't remove a column
                rnd_choice = 1
            else:
                rnd_choice = random.randint(1,100) # decides to make a move (1-50) or remove a column (51-100)
        else: # the agent already removed a column
            rnd_choice = 1

        if rnd_choice <= 50:  # making a move - placing a piece
            rnd_place = random.randint(0, len(self.legal_empty) - 1)  # picks a random number that represents the index in the list of legal moves
            place = self.legal_empty[rnd_place]
            self.board[place[0], place[1]] = self.player # places the piece of the player on the board in the chosen place
            if place[0] > 0: # if there is a place above the current cell
                self.legal_empty.append((place[0] - 1, place[1]))  # adds the place above the current place to list of empty legal places
            self.legal_empty.remove(place)  # removes the place from the list of the legal empty places
            self.last_move = place, self.player # the last move - the  index of the place and the number of the agent

        else:  # removing a column
            self.removeColumn()
            self.col_remove_player = False # changes the feature to "False" to not be able to remove another one
            self.last_move = (5, 7), self.player # the last move - index out of the board range represents the removing of column

    def smartPlayer(self):
        # heuristics

        max_grade = 0 # saves the highest grade
        first_board_flag = True # checks if it's the first board
        place = None

        for option in self.legal_empty: # goes over the cells in the list of empty legal places
            temp_board = copy.deepcopy(self.board) # copies the current board
            temp_board[option[0],option[1]] = -1 # changes the board in the current empty cell

            current_grade = 0 # the sum grade
            current_grade += self.findInCols(temp_board,self.player) # goes over the columns and searches for player
            current_grade += self.findInCols(temp_board, self.agent) # goes over the columns and searches for agent
            current_grade += self.findInRows(temp_board, self.player) # goes over the rows and searches for player
            current_grade += self.findInRows(temp_board, self.agent) # goes over the rows and searches for agent
            current_grade += self.findInMainDiagonal(temp_board, self.player) # goes over the main diagonal and searches for player
            current_grade += self.findInMainDiagonal(temp_board, self.agent) # goes over the main diagonal and searches for agent
            current_grade += self.findInAntiDiagonal(temp_board, self.player) # goes over the anti-diagonal and searches for player
            current_grade += self.findInAntiDiagonal(temp_board, self.agent) # goes over the anti-diagonal and searches for agent

            if first_board_flag: # if it's the first board
                max_grade = current_grade
                place = option
                first_board_flag = False
            elif current_grade > max_grade:  # if this grade is higher than the current max
                max_grade = current_grade
                place = option  # saves the empty cell

        # if the player still hasn't removed a column
        if self.col_remove_player:
            for column in self.legal_empty: # goes over the empty legal places
                if column[0] < 4: # if the empty place is not in the bottom row - this column can be removed
                    temp_board = copy.deepcopy(self.board) # copies the current board
                    for i in range(5): # goes over the chosen column and disables the rows
                        temp_board[i,column[1]] = -2

                    current_grade = 0  # the sum grade
                    current_grade += self.findInCols(temp_board,self.player)  # goes over the columns and searches for player
                    current_grade += self.findInCols(temp_board,self.agent)  # goes over the columns and searches for agent
                    current_grade += self.findInRows(temp_board,self.player)  # goes over the rows and searches for player
                    current_grade += self.findInRows(temp_board,self.agent)  # goes over the rows and searches for agent
                    current_grade += self.findInMainDiagonal(temp_board,self.player)  # goes over the main diagonal and searches for player
                    current_grade += self.findInMainDiagonal(temp_board,self.agent)  # goes over the main diagonal and searches for agent
                    current_grade += self.findInAntiDiagonal(temp_board,self.player)  # goes over the anti-diagonal and searches for player
                    current_grade += self.findInAntiDiagonal(temp_board,self.agent)  # goes over the anti-diagonal and searches for agent

                    if current_grade > max_grade:  # if this grade is higher than the current max
                        max_grade = current_grade
                        num_col = column[1]  # saves the possible removed column
                        place = (5, 7)  # the saved place is out of the range of the board - to mark a remove of a column

        if place is None:
            self.playerTurn()
        elif place[0] == 5:  # if the saved place was (5,7) there is going to be a column removed
            for row in range(5):  # goes over all the rows in the removed column and disables them
                cell = (row, num_col)  # the current cell
                self.board[cell[0],cell[1]] = -2  # disabling the cell
                if cell in self.legal_empty:  # if the cell was empty and legal for a move it's removed from the list
                    self.legal_empty.remove(cell)
            self.col_remove_player = False  # changes the feature to "False" to not be able to remove another one
            self.last_move = place, self.player  # the last move - index out of the board range represents the removing of column
        else:  # the removed cell is an empty place on the board
            self.board[place[0], place[1]] = self.player  # places the piece of the player on the board in the chosen place
            if place[0] > 0:  # if there is a place above the current cell
                self.legal_empty.append((place[0]-1, place[1]))  # adds the place above the current place to list of empty legal places
            self.legal_empty.remove(place)  # removes the place from the list of the legal empty places
            self.last_move = place, self.player  # the last move - the  index of the place and the number of the player

    def findInCols(self,temp_board,current):
        grade = 0 # the sum of grade
        for c in range (7): # goes over the columns
            count_sequence = 0 # counts the length of a sequence
            count_empty = 0
            for r in range (4,-1,-1): # starts from the bottom row and counts the sequence
                if temp_board[r][c] == current:
                    if count_empty == 0: # the sequence hasn't stopped yet
                        count_sequence += 1
                    else: break # if the sequence stopped the loop stops
                elif temp_board[r][c] == 0:
                    count_empty += 1
            if current == self.agent: # checking for agent:
                if count_sequence == 3 and count_empty > 0: # sequence of 3 and 1 empty
                    grade += self.agent3grade
                elif count_sequence == 2 and count_empty > 1: # sequence of 2 and 2 empty
                    grade += self.agent2grade
            if current == self.player: # checking for player:
                if count_sequence == 3 and count_empty > 0: # sequence of 3 and 1 empty
                    grade += self.player3grade
                elif count_sequence == 2 and count_empty > 1: # sequence of 2 and 2 empty
                    grade += self.player2grade
        return grade

    def findInRows(self,temp_board, current):
        grade = 0
        for r in range (5):
            for i in range (4):
                count_sequence = 0
                count_empty = 0
                for c in range (4):
                    if temp_board[r][c+i] == current:
                        count_sequence += 1
                    elif temp_board[r][c+i] == 0:
                        count_empty += 1
                    else: break
                if current == self.agent:  # checking for agent:
                    if count_sequence == 3 and count_empty > 0:  # sequence of 3 and 1 empty
                        grade += self.agent3grade
                    elif count_sequence == 2 and count_empty > 1:  # sequence of 2 and 2 empty
                        grade += self.agent2grade
                if current == self.player:  # checking for player:
                    if count_sequence == 3 and count_empty > 0:  # sequence of 3 and 1 empty
                        grade += self.player3grade
                    elif count_sequence == 2 and count_empty > 1:  # sequence of 2 and 2 empty
                        grade += self.player2grade
        return grade

    def findInAntiDiagonal(self,temp_board,current):
        grade = 0
        row = 3
        for col in range (4):
            count_sequence = 0
            count_empty = 0
            for i in range (4):
                if temp_board[row-i][col+i] == current:
                    count_sequence += 1
                elif temp_board[row-i][col+i] == 0:
                    count_empty += 1
                else: break
            if current == self.agent: # checking for agent:
                if count_sequence == 3 and count_empty > 0: # sequence of 3 and 1 empty
                    grade += self.agent3grade
                elif count_sequence == 2 and count_empty > 1: # sequence of 2 and 2 empty
                    grade += self.agent2grade
            if current == self.player: # checking for player:
                if count_sequence == 3 and count_empty > 0: # sequence of 3 and 1 empty
                    grade += self.player3grade
                elif count_sequence == 2 and count_empty > 1: # sequence of 2 and 2 empty
                    grade += self.player2grade

        row = 4
        for col in range(4):
            count_sequence = 0
            count_empty = 0
            for i in range(4):
                if temp_board[row - i][col + i] == current:
                    count_sequence += 1
                elif temp_board[row - i][col + i] == 0:
                    count_empty += 1
                else: break
            if current == self.agent:  # checking for agent:
                if count_sequence == 3 and count_empty > 0:  # sequence of 3 and 1 empty
                    grade += self.agent3grade
                elif count_sequence == 2 and count_empty > 1:  # sequence of 2 and 2 empty
                    grade += self.agent2grade
            if current == self.player:  # checking for player:
                if count_sequence == 3 and count_empty > 0:  # sequence of 3 and 1 empty
                    grade += self.player3grade
                elif count_sequence == 2 and count_empty > 1:  # sequence of 2 and 2 empty
                    grade += self.player2grade

        return grade

    def findInMainDiagonal(self,temp_board,current):
        grade = 0
        row = 0
        for col in range(4):
            count_sequence = 0
            count_empty = 0
            for i in range (4):
                if temp_board[row+i][col+i] == current:
                    count_sequence += 1
                elif temp_board[row+i][col+i] == 0:
                    count_empty += 1
                else: break
            if current == self.agent:
                if count_sequence == 3 and count_empty > 0:
                    grade += self.agent3grade
                elif count_sequence == 2 and count_empty > 1:
                    grade += self.agent2grade
            if current == self.player:
                if count_sequence == 3 and count_empty > 0:
                    grade += self.player3grade
                elif count_sequence == 2 and count_empty > 1:
                    grade += self.player2grade

        row = 1
        for col in range(4):
            count_sequence = 0
            count_empty = 0
            for i in range (4):
                if temp_board[row+i][col+i] == current:
                    count_sequence += 1
                elif temp_board[row+i][col+i] == 0:
                    count_empty += 1
                else: break
            if current == self.agent:
                if count_sequence == 3 and count_empty > 0:
                    grade += self.agent3grade
                elif count_sequence == 2 and count_empty > 1:
                    grade += self.agent2grade
            if current == self.player:
                if count_sequence == 3 and count_empty > 0:
                    grade += self.player3grade
                elif count_sequence == 2 and count_empty > 1:
                    grade += self.player2grade

        return grade

    def removeColumn(self):
        # removes a full column and disables all the cells
        flag_col = False  # checks if the column is empty
        rnd_col = random.randint(0, 6)  # picks a random column
        while not flag_col:  # goes over the random columns until it picks a none empty one
            if (4, rnd_col) not in self.legal_empty and self.board[4, rnd_col] != -2:
                # if the lowest cell in the random column isn't empty and wasn't already removed the column can be removed
                flag_col = True
            else:
                rnd_col = random.randint(0, 6)  # if the column is empty the random chooses again
        for row in range(5):  # goes over all the rows in the removed column and disables them
            place = (row, rnd_col)  # the current cell
            self.board[place[0], place[1]] = -2  # disabling the cell
            if place in self.legal_empty:  # if the cell was empty and legal for a move it's removed from the list
                self.legal_empty.remove(place)

    def checkWin(self):
        row = self.last_move[0][0]
        col = self.last_move[0][1]

        if row == 5: # if the row is 5 it means the last move was removing a column - can't be a win
            return 0

        else:
            # goes over the row of the last move and checks for a win
            count = 1 # counts the length of the potential sequence
            for i in range (col+1,7): # goes over all the cells to the right of the last move
                if self.board[row, i] == self.last_move[1]:
                    count += 1
                else: break # if the sequence stops the loop stops
            for i in range (col-1,-1,-1): # goes over all the cells to the left of the last move
                if self.board[row, i] == self.last_move[1]:
                    count += 1
                else: break # if the sequence stops the loop stops
            if count >= 4: # if there is a 4 pieces sequence - there is a win
                return self.last_move[1]

            # goes over the column of the last move and checks for a win
            count = 1 # counts the length of the potential sequence
            for i in range (row+1,5): # goes over all the cells below the last move
                if self.board[i, col] == self.last_move[1]:
                    count += 1
                else: break # if the sequence stops the loop stops
            for i in range (row-1,-1,-1): # goes over all the cells above the last move
                if self.board[i, col] == self.last_move[1]:
                    count += 1
                else: break # if the sequence stops the loop stops
            if count >= 4: # if there is a 4 pieces sequence - there is a win
                return self.last_move[1]

            # goes over the main diagonal that's part of the last move
            count = 1 # counts the length of the potential sequence
            # moving towards the up right corner - row-1, col+1
            j = col # moves over the columns
            for i in range(row-1,-1,-1): # moves over the rows
                # goes over the cells towards the up right corner of the board
                if j > 6 or self.board[i, j] != self.last_move[1]: # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j += 1
            # moving towards the down left corner - row+1, col-1
            j = col-1 # moves over the columns
            for i in range (row+1,5): # moves over the rows
                # goes over the cells towards the down left corner of the board
                if j < 0 or self.board[i, j] != self.last_move[1]: # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j -= 1
            if count >= 4: # if there is a 4 pieces sequence - there is a win
                return self.last_move[1]

            # goes over the anti-diagonal that's part of the last move
            count = 1 # counts the length of the potential sequence
            # moving towards the up left corner - row-1, col-1
            j = col # moves over the columns
            for i in range(row-1,-1,-1): # moves over the rows
                # goes over the cells towards the up left corner of the board
                if j < 0 or self.board[i, j] != self.last_move[1]: # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j -= 1
            # moving towards the down right corner - row+1, col+1
            j = col+1 # moves over the columns
            for i in range (row+1,5): # moves over the rows
                # goes over the cells towards the down left corner of the board
                if j > 6 or self.board[i, j] != self.last_move[1]: # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j += 1
            if count >= 4: # if there is a 4 pieces sequence - there is a win
                return self.last_move[1]

        return 0

    def printBoard(self):
        print(self.board,"\n")

    def tie(self):
        if len(self.legal_empty) == 0 and self.checkWin() == 0:
            return True
        return False

    def found_winner(self):
        if self.checkWin() == 0:
            return False
        return True

    def playOneGame(self):
        self.smartAgent()
        #self.printBoard()
        self.all_game_boards.append(self.boardToString(self.board)) # turning the board into a string and adding to a list of all the boards in the game
        #self.smartPlayer()
        self.playerTurn()
        #self.printBoard()
        self.all_game_boards.append(self.boardToString(self.board)) # turning the board into a string and adding to a list of all the boards in the game

        while self.found_winner() == False and self.tie() == False:
            self.smartAgent()
            #self.printBoard()
            self.all_game_boards.append(self.boardToString(self.board)) # turning the board into a string and adding to a list of all the boards in the game
            if self.checkWin() == self.agent:
                #print ("the winner is agent")
                #self.printBoard()
                self.winner = self.agent
            elif self.tie() == False:
                #self.smartPlayer()
                self.playerTurn()
                #self.printBoard()
                self.all_game_boards.append(self.boardToString(self.board)) # turning the board into a string and adding to a list of all the boards in the game
                if self.checkWin() == self.player:
                    #print ("the winner is player")
                    #self.printBoard()
                    self.winner = self.player
            else:
                #print("tie")
                #self.printBoard()
                self.winner = 0

        self.grading() # the process of grading each board for RL

    def boardToString(self, current_board):
        # goes from board to a string - agent: X, player: O, empty: -, disabled: =
        stringBoard = ""
        count = 0 # counts how many non-empty cells are on the board, to separate the dictionary
        for i in range (5):
            for j in range (7):
                if current_board[i][j] == -1:
                    stringBoard += "O"
                    count += 1
                elif current_board[i][j] == 1:
                    stringBoard += "X"
                    count += 1
                elif current_board[i][j] == -2:
                    stringBoard += "="
                    count += 1
                else:
                    stringBoard += "-"
        return stringBoard, count

    def grading(self):
        # grades each board to create a reinforcement learning system
        num_of_board = len(self.all_game_boards)-1 # the number of the current board, the first one will be the winning board
        # the grade is assigned based on who won the game
        if self.winner == self.agent:
            grade = self.grade_agent
        elif self.winner == self.player:
            grade = self.grade_player
        else:
            grade = self.grade_tie

        self.boards_and_grades = [(self.all_game_boards[num_of_board][0], grade, self.all_game_boards[num_of_board][1])]
        # adds the winning board to the list of boards+grades+count of non-empty cells
        for i in range (num_of_board-1,-1,-1):
            # goes over the boards of the game from last to first and grades them
            grade = grade * self.gamma # the calculation of the grade - (the last grade)*(gamma)
            self.boards_and_grades.append((self.all_game_boards[i][0], grade, self.all_game_boards[i][1]))
            # adds the board and its grade to the list (and count of non-empty cells)

class Games:
    def __init__(self):
        #self.my_dict1 = {}
        #self.my_dict2 = {}
        #self.my_dict3 = {}
        #self.my_dict4 = {}
        #self.my_dict5 = {}
        with open('Dictionaries2/dict1_18.json', 'r') as json_file:
            self.my_dict1 = json.load(json_file)
        # dictionary that contains the boards, their grade, and how many times they appeared (1-18 non-empty places)
        with open('Dictionaries2/dict19_21.json', 'r') as json_file:
            self.my_dict2 = json.load(json_file)
        # dictionary that contains the boards, their grade, and how many times they appeared (19-21 non-empty places)
        with open('Dictionaries2/dict22_25.json', 'r') as json_file:
            self.my_dict3 = json.load(json_file)
        # dictionary that contains the boards, their grade, and how many times they appeared (22-25 non-empty places)
        with open('Dictionaries2/dict26_29.json', 'r') as json_file:
            self.my_dict4 = json.load(json_file)
        # dictionary that contains the boards, their grade, and how many times they appeared (26-29 non-empty places)
        with open('Dictionaries2/dict30_35.json', 'r') as json_file:
            self.my_dict5 = json.load(json_file)
        # dictionary that contains the boards, their grade, and how many times they appeared (30-35 non-empty places)

    def create_data(self):
        count_agent_wins = 0
        for g in range(100000):
            # runs 100,000 times to create a database in a dictionary
            game = Game()
            game.playOneGame()
            if game.winner == 1:
                count_agent_wins += 1
                for i in range(len(game.boards_and_grades)):
                    # goes over the list of boards and grades from the current game and adds it to the dictionary
                    board = game.boards_and_grades[i][0]
                    grade = game.boards_and_grades[i][1]
                    count = game.boards_and_grades[i][2]

                    # saving the boards into the dictionaries and separating the by the number of non-empty places on the board
                    if 0 < count < 19:
                        if board in games.my_dict1:
                            # if this board already exists in the dictionary - the saved grade is an average of all the grades of this board
                            last_count = self.my_dict1[board][1]  # count of times this board already appeared
                            last_avg = self.my_dict1[board][0] * last_count  # the saved grade times the count (to find the sum of all grades)
                            self.my_dict1[board] = ((last_avg + grade) / (last_count + 1), last_count + 1)
                            # 1 - average grade of the board, 2 - count of times the board appeared, including this time
                        else:
                            # if this board doesn't exist in the dictionary yet
                            self.my_dict1[board] = (grade, 1)

                    if 18 < count < 22:
                        if board in games.my_dict1:
                            # if this board already exists in the dictionary - the saved grade is an average of all the grades of this board
                            last_count = self.my_dict2[board][1]  # count of times this board already appeared
                            last_avg = self.my_dict2[board][0] * last_count  # the saved grade times the count (to find the sum of all grades)
                            self.my_dict2[board] = ((last_avg + grade) / (last_count + 1), last_count + 1)
                            # 1 - average grade of the board, 2 - count of times the board appeared, including this time
                        else:
                            # if this board doesn't exist in the dictionary yet
                            self.my_dict2[board] = (grade, 1)

                    if 21 < count < 26:
                        if board in games.my_dict1:
                            # if this board already exists in the dictionary - the saved grade is an average of all the grades of this board
                            last_count = self.my_dict3[board][1]  # count of times this board already appeared
                            last_avg = self.my_dict3[board][0] * last_count  # the saved grade times the count (to find the sum of all grades)
                            self.my_dict3[board] = ((last_avg + grade) / (last_count + 1), last_count + 1)
                            # 1 - average grade of the board, 2 - count of times the board appeared, including this time
                        else:
                            # if this board doesn't exist in the dictionary yet
                            self.my_dict3[board] = (grade, 1)

                    if 25 < count < 30:
                        if board in games.my_dict1:
                            # if this board already exists in the dictionary - the saved grade is an average of all the grades of this board
                            last_count = self.my_dict4[board][1]  # count of times this board already appeared
                            last_avg = self.my_dict4[board][0] * last_count  # the saved grade times the count (to find the sum of all grades)
                            self.my_dict4[board] = ((last_avg + grade) / (last_count + 1), last_count + 1)
                            # 1 - average grade of the board, 2 - count of times the board appeared, including this time
                        else:
                            # if this board doesn't exist in the dictionary yet
                            self.my_dict4[board] = (grade, 1)

                    if 29 < count < 36:
                        if board in games.my_dict1:
                            # if this board already exists in the dictionary - the saved grade is an average of all the grades of this board
                            last_count = self.my_dict5[board][1]  # count of times this board already appeared
                            last_avg = self.my_dict5[board][0] * last_count  # the saved grade times the count (to find the sum of all grades)
                            self.my_dict5[board] = ((last_avg + grade) / (last_count + 1), last_count + 1)
                            # 1 - average grade of the board, 2 - count of times the board appeared, including this time
                        else:
                            # if this board doesn't exist in the dictionary yet
                            self.my_dict5[board] = (grade, 1)

        # saving all the dictionaries into json files
        with open('Dictionaries2/dict1_18.json', 'w') as json_file:
            json.dump(self.my_dict1, json_file)
        with open('Dictionaries2/dict19_21.json', 'w') as json_file:
            json.dump(self.my_dict2, json_file)
        with open('Dictionaries2/dict22_25.json', 'w') as json_file:
            json.dump(self.my_dict3, json_file)
        with open('Dictionaries2/dict26_29.json', 'w') as json_file:
            json.dump(self.my_dict4, json_file)
        with open('Dictionaries2/dict30_35.json', 'w') as json_file:
            json.dump(self.my_dict5, json_file)

        print("agent:", count_agent_wins / 1000, "%")

    # checking the dictionary
    def print_start_grades(self):
        # goes over the dictionary and prints the grade of each staring board
        for board, (grade, occurrences) in self.my_dict1.items():
            # goes over the items in the dictionary
            if board.count("-") == 34:
                # if the board has exactly 34 empty cells it means it's a starting board
                print ("for starting board ", board,", the grade is: ",grade)


games = Games()
#games.create_data()
#games.print_start_grades()

g = Game()
g.playOneGame()

"""
count_win = 0
for i in range (1000):
    g = Game()
    g.playOneGame()
    if g.winner == 1:
        count_win += 1
print(count_win)
"""
