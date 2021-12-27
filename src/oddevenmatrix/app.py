# -*- coding: utf-8 -*-
"""
一个简单的数字棋盘游戏
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def defineSquare(size: int = 9) -> list:
    square = []
    for i in range(size):
        square.append([])
        for j in range(size):
            square[i].append(None)
    return square


def couldPlace(square: list, pos: list, num: int):
    num = isDouble(num)
    # print(str(num))
    # only line & row
    for i in range(len(square)):
        print(str(i)+','+str(pos[1]))
        if square[i][pos[1]] and square[i][pos[1]] != num:
            return False
    for j in range(len(square[pos[0]])):
        print(str(pos[0])+' '+str(j))
        if square[pos[0]][j] and square[pos[0]][j] != num:
            return False
    i = pos[0]
    j1 = pos[1]
    j2 = pos[1]
    while i >= 0:
        print(str(i)+':'+str(j1))
        print(str(i)+':'+str(j2))
        if j1 >= 0:
            if square[i][j1] and square[i][j1] != num:
                return False
        if j2 <= len(square[i])-1:
            if square[i][j2] and square[i][j2] != num:
                return False
        j1 -= 1
        j2 += 1
        i -= 1
    i = pos[0]
    j1 = pos[1]
    j2 = pos[1]
    while i <= len(square)-1:
        print(str(i)+'`'+str(j1))
        print(str(i)+'`'+str(j2))
        if j1 >= 0:
            if square[i][j1] and square[i][j1] != num:
                return False
        if j2 <= len(square[i])-1:
            if square[i][j2] and square[i][j2] != num:
                return False
        j1 -= 1
        j2 += 1
        i += 1
    square[pos[0]][pos[1]] = num
    return square


def isDouble(n: int):
    if n % 2 == 0:
        return 2
    else:
        return 1


def formatBoard(realBoard: list) -> list:
    bar = []
    boardBar = '  '
    for i in range(len(realBoard)):
        boardBar += str(i)+'|'
    print(boardBar)
    bar.append(boardBar)
    boardBar = ''
    for i in range(len(realBoard)):
        boardBar += str(i)+'|'
        for j in range(len(realBoard)):
            if realBoard[i][j]:
                boardBar += str(realBoard[i][j])+' '
            else:
                boardBar += '□'
        print(boardBar)
        bar.append(boardBar)
        boardBar = ''
    return bar


def makeDetailedList(formattedRealBoard: list):
    dlist = []
    for i in formattedRealBoard:
        dlist.append({'icon': '',
                      'title': '-',
                      'subtitle': i,
                      'pk': 100
                      })
    return dlist


defaultSize = 9


class OddEvenMatrix(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        # The main function start up
        board = defineSquare(defaultSize)
        realBoard = defineSquare(defaultSize)

        notBeenPlaced = {
            1: list(range(1, defaultSize+1)),
            2: list(range(1, defaultSize+1))
        }

        nowPlayer = 1

        # Start to draw the window

        main_box = toga.Box(style=Pack(direction=COLUMN))

        self.noticeLabel = toga.Label(
            '执行 >>>',
            style=Pack(padding=(0, 5))
        )
        self.inputBox = toga.TextInput(style=Pack(flex=1))
        #dispImage = toga.ImageView("./resources/oddevenmatrix.png")

        cmd_box = toga.Box(style=Pack(direction=ROW, padding=5))
        cmd_box.add(self.noticeLabel)
        cmd_box.add(self.inputBox)
        # cmd_box.add(dispImage)

        button = toga.Button(
            'Run',
            on_press=self.runrun,
            style=Pack(padding=5)
        )
        self.dispLabel = toga.DetailedList(data=makeDetailedList(formatBoard(realBoard)),)

        main_box.add(cmd_box)
        main_box.add(button)
        main_box.add(self.dispLabel)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def runrun(self, widget):
        self.dispLabel._impl.set_text(self.inputBox.value)


def main():
    return OddEvenMatrix()
