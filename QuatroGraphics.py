from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import random
import json

class FirstScreen(FloatLayout):
    def __init__(self):
        FloatLayout.__init__(self)
        self.graphBoard = Board()
        self.addOn()
        self.addButton()

    def addOn(self):
        self.graphBoard.size_hint = (.5, .5)
        self.graphBoard.pos_hint = {"center_x": .5, "center_y": .7}
        self.add_widget(self.graphBoard)

    def addButton(self):
        self.buttonRestart = Button()
        self.buttonRestart.text = "refresh"
        self.buttonRestart.pos_hint = {"center_x": .1, "center_y": .2}
        self.buttonRestart.size_hint = (.2, .1)
        self.buttonRestart.bind(on_press = self.restart)
        self.add_widget(self.buttonRestart)

    def restart(self, touched):
        self.graphBoard.restart()
        self.graphBoard.agent()

class Cell(Button):  # MAKING A BUTTON WITH A '?' PICTURE
    def __init__(self, row, col):
        Button.__init__(self)
        self.text = "?"
        self.row = row
        self.col = col

    def on_press(self):
        answer = self.parent.check(self.row, self.col)
        if answer:
            self.text = "O"
            self.parent.react()

class Board(GridLayout):  # Making 3*3 board with question marks
    def __init__(self):
        GridLayout.__init__(self)
        self.cols = 7
        self.listGraphBoard = []
        self.controller = Controller()
        self.addCellsToBoard()
        self.create_announce()
        self.agent()

    def agent(self):
       place = self.controller.agent()
       if place[0] >= 5:
           for row in range(5):
               self.listGraphBoard[row][place[1]].text = "="
               self.listGraphBoard[row][place[1]].disabled = True
       else:
            self.listGraphBoard[place[0]][place[1]].text = "X"

    def smartAgent(self):
       place = self.controller.smartAgent()
       self.listGraphBoard[place[0]][place[1]].text = "X"

    def react(self):
        if self.controller.checkWin():
            self.announcement(-1)
            self.disabled = True
            print("player win")
        else:
            if self.controller.checkTie():
                self.disabled = True
                self.announcement(0)
                print("tie")
            else:
                self.agent()
                if self.controller.checkWin():
                    self.announcement(1)
                    self.disabled = True
                    print("agent win")
                else:
                    if self.controller.checkTie():
                        self.disabled = True
                        self.announcement(0)
                        print("tie")

    def addCellsToBoard(self):
        for line in range(5):
            newLine = []
            for col in range(7):
                temp_cell = Cell(line, col)
                self.add_widget(temp_cell)
                newLine.append(temp_cell)
            self.listGraphBoard.append(newLine)

    def check(self, row, col):
        return self.controller.check(row, col)

    def announcement(self,current_move):
        if current_move == 1:
            self.announce.text = "Game Over! Agent Won The Game!"
        elif current_move == -1:
            self.announce.text = "Game Over! Player Won The Game!"
        else:
            self.announce.text = "Game Over! No One Wins"

    def create_announce(self):
        self.announce = Label()
        self.announce.font_size = 30
        self.announce.text = " "
        self.add_widget(self.announce)

    def restart(self):
        self.announce.text = " "
        for row in range(5):
            for col in range(7):
                self.listGraphBoard[row][col].text = "?"
        self.disabled = False
        return self.controller.restart()


class Controller():
    def __init__(self):
        self.logic = Logic()

    def check(self, row, col):
        return self.logic.check(row, col)

    def smartAgent(self):
        return self.logic.smartAgent()

    def agent(self):
        return self.logic.agentTurn()

    def checkWin(self):
        return self.logic.checkWin()

    def checkTie(self):
        return self.logic.tie()

    def restart(self):
        return self.logic.restart()


class Logic():
    def __init__(self):
        # 0 : empty, 1 : X agent, -1 : O player, -2 : = disabled
        self.board = [[0 for _ in range(7)] for _ in range(5)] # board of 5 rows and 7 columns
        self.legal_empty = self.legalMove() # list of empty places where you can place a legal move
        self.last_move = ((0, 0), 0)
        self.col_remove_agent = True  # True - agent didn't remove a column yet, False - already removed a column
        self.col_remove_player = True  # True - player didn't remove a column yet, False - already removed a column

        #with open('dict_boards.json', 'r') as json_file:
        #   self.my_dict = json.load(json_file)

    def check(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = -1
            if row > 0: # if there is a place above the current cell
                self.legal_empty.append((row-1, col))  # adds the place above the current place to list of empty legal places
            self.legal_empty.remove((row,col)) # removes the place from the list of the legal empty places
            self.last_move = (row,col), -1 # the last move - the  index of the place and the number of the agent
            return True
        else:
            return False

    def legalMove(self):
        # creates a list of all the empty places you can place a move on
        self.legal_empty = []
        for i in range (7):
            # goes over all the columns and adds the bottom cell to the list
            self.legal_empty.append((4,i))
        return self.legal_empty

    def boardToString(self,current_board):
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

    def checkWin(self):
        row = self.last_move[0][0]
        col = self.last_move[0][1]

        if row == 5:  # if the row is 5 it means the last move was removing a column - can't be a win
            return False

        else:
            # goes over the row of the last move and checks for a win
            count = 1  # counts the length of the potential sequence
            for i in range(col + 1, 7):  # goes over all the cells to the right of the last move
                if self.board[row][i] == self.last_move[1]:
                    count += 1
                else:
                    break  # if the sequence stops the loop stops
            for i in range(col - 1, -1, -1):  # goes over all the cells to the left of the last move
                if self.board[row][i] == self.last_move[1]:
                    count += 1
                else:
                    break  # if the sequence stops the loop stops
            if count >= 4:  # if there is a 4 pieces sequence - there is a win
                return True

            # goes over the column of the last move and checks for a win
            count = 1  # counts the length of the potential sequence
            for i in range(row + 1, 5):  # goes over all the cells below the last move
                if self.board[i][col] == self.last_move[1]:
                    count += 1
                else:
                    break  # if the sequence stops the loop stops
            for i in range(row - 1, -1, -1):  # goes over all the cells above the last move
                if self.board[i][col] == self.last_move[1]:
                    count += 1
                else:
                    break  # if the sequence stops the loop stops
            if count >= 4:  # if there is a 4 pieces sequence - there is a win
                return True

            # goes over the main diagonal that's part of the last move
            count = 1  # counts the length of the potential sequence
            # moving towards the up right corner - row-1, col+1
            j = col  # moves over the columns
            for i in range(row - 1, -1, -1):  # moves over the rows
                # goes over the cells towards the up right corner of the board
                if j > 6 or self.board[i][j] != self.last_move[1]:  # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j += 1
            # moving towards the down left corner - row+1, col-1
            j = col - 1  # moves over the columns
            for i in range(row + 1, 5):  # moves over the rows
                # goes over the cells towards the down left corner of the board
                if j < 0 or self.board[i][j] != self.last_move[1]:  # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j -= 1
            if count >= 4:  # if there is a 4 pieces sequence - there is a win
                return True

            # goes over the anti-diagonal that's part of the last move
            count = 1  # counts the length of the potential sequence
            # moving towards the up left corner - row-1, col-1
            j = col  # moves over the columns
            for i in range(row - 1, -1, -1):  # moves over the rows
                # goes over the cells towards the up left corner of the board
                if j < 0 or self.board[i][j] != self.last_move[
                    1]:  # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j -= 1
            # moving towards the down right corner - row+1, col+1
            j = col + 1  # moves over the columns
            for i in range(row + 1, 5):  # moves over the rows
                # goes over the cells towards the down left corner of the board
                if j > 6 or self.board[i][j] != self.last_move[
                    1]:  # if the cell is not on the board or breaking the sequence the loop stops
                    break
                count += 1
                j += 1
            if count >= 4:  # if there is a 4 pieces sequence - there is a win
                return True

        return False

    def tie(self):
        if len(self.legal_empty) == 0 and self.checkWin() == 0:
            return True
        return False

    def restart(self):
        self.board = [[0 for _ in range(7)] for _ in range(5)]  # board of 5 rows and 7 columns
        self.legal_empty = self.legalMove()  # list of empty places where you can place a legal move
        self.last_move = ((0, 0), 0) # last place on board where a move was made, who made the move
        return True

    def agentTurn(self):
        if self.col_remove_agent: # if the agent didn't remove a column yet
            count = 0 # counts the empty columns
            for col in range (7):
                # goes over the lowest row and checks if it's empty
                if (4,col) in self.legal_empty or self.board[4][col] == -2: # if the column is empty or already removed the count goes up
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
            self.board[place[0]][place[1]] = 1 # places the piece of the agent on the board in the chosen place
            if place[0] > 0 : # if there is a place above the current cell
                self.legal_empty.append((place[0]-1,place[1])) # adds the place above the current place to list of empty legal places
            self.legal_empty.remove(place) # removes the place from the list of the legal empty places
            self.last_move = place, 1 # the last move - the  index of the place and the number of the agent
            return place

        else: # removing a column
            col_remove = self.removeColumn()
            self.col_remove_agent = False # changes the feature to "False" to not be able to remove another one
            self.last_move = (5,col_remove), 1 # the last move - index out of the board range represents the removing of column

    def removeColumn(self):
        # removes a full column and disables all the cells
        flag_col = False  # checks if the column is empty
        rnd_col = random.randint(0, 6)  # picks a random column
        while not flag_col:  # goes over the random columns until it picks a none empty one
            if (4, rnd_col) not in self.legal_empty and self.board[4][rnd_col] != -2:
                # if the lowest cell in the random column isn't empty and wasn't already removed the column can be removed
                flag_col = True
            else:
                rnd_col = random.randint(0, 6)  # if the column is empty the random chooses again
        for row in range(5):  # goes over all the rows in the removed column and disables them
            place = (row, rnd_col)  # the current cell
            self.board[place[0]][place[1]] = -2  # disabling the cell
            if place in self.legal_empty:  # if the cell was empty and legal for a move it's removed from the list
                self.legal_empty.remove(place)
        return rnd_col

class MyPaintApp(App):
    def build(self):
        return FirstScreen()


MyPaintApp().run()
