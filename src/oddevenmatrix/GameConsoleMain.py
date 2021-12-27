# -*- coding: utf-8 -*-

# 生命灵动，当用激情跃起奋发之力

# 奇偶数阵

# 学海无涯 应用爱意徜徉
# 在生命的起源寻找灵魂的慰藉


import os
import sys
from msvcrt import getch


def defineSquare(size: int = 9):
    square = []
    for i in range(size):
        square.append([])
        for j in range(size):
            square[i].append(None)
    return square


def couldPlace(square: list, pos: list, num: int):
    '''返回是否能够放置棋子，若不能，则返回`False`，若能够，则返回放置后的源盘
    :param square:list  当前的源盘（SourceBoard）
    :param pos:list     需要判定的位置
    :param num:int      需要判定的数字'''
    num = isDouble(num)
    # print(str(num))
    # only line & row
    if square[pos[0]][pos[1]] and square[pos[0]][pos[1]] != num:
        return False
    if num == 1:
        square[pos[0]][pos[1]] = '奇'
    if num == 2:
        square[pos[0]][pos[1]] = '偶'

    for i in range(len(square)):
        # 遍历行
        print(str(i)+','+str(pos[1]))
        if square[i][pos[1]] and square[i][pos[1]] != num:
            square[i][pos[1]] = '空'
        else:
            square[i][pos[1]] = num
    for j in range(len(square[pos[0]])):
        # 遍历对应列
        print(str(pos[0])+' '+str(j))
        if square[pos[0]][j] and square[pos[0]][j] != num:
            square[pos[0]][j] = '空'
        else:
            square[pos[0]][j] = num
    i = pos[0]
    j1 = pos[1]
    j2 = pos[1]
    while i >= 0:
        # 遍历上半部分斜线
        print(str(i)+':'+str(j1))
        print(str(i)+':'+str(j2))
        if j1 >= 0:
            if square[i][j1] and square[i][j1] != num:
                square[i][j1] = '空'
            else:
                square[i][j1] = num
        if j2 <= len(square[i])-1:
            if square[i][j2] and square[i][j2] != num:
                square[i][j2] = '空'
            else:
                square[i][j2] = num
        j1 -= 1
        j2 += 1
        i -= 1
    i = pos[0]
    j1 = pos[1]
    j2 = pos[1]
    while i <= len(square)-1:
        # 遍历下半部分斜线
        print(str(i)+'`'+str(j1))
        print(str(i)+'`'+str(j2))
        if j1 >= 0:
            if square[i][j1] and square[i][j1] != num:
                square[i][j1] = '空'
            else:
                square[i][j1] = num
        if j2 <= len(square[i])-1:
            if square[i][j2] and square[i][j2] != num:
                square[i][j2] = '空'
            else:
                square[i][j2] = num
        j1 -= 1
        j2 += 1
        i += 1

    return square


def isDouble(n: int):
    if n % 2 == 0:
        return 2
    else:
        return 1


def printBoard(realBoard: list, sourceBoard: list, select: list):

    boardBar = '  '
    for i in range(len(realBoard)):
        boardBar += str(i)+'|'
    print(boardBar)
    boardBar = ''
    for i in range(len(realBoard)):
        boardBar += str(i)+'|'
        for j in range(len(realBoard)):
            if realBoard[i][j]:
                boardBar += str(realBoard[i][j])+' '
            else:
                if i == select[0] and j == select[1]:
                    boardBar += '[]'
                else:
                    if sourceBoard[i][j]==1:
                        boardBar += '奇'
                    elif sourceBoard[i][j]==2:
                        boardBar += '偶'
                    elif sourceBoard[i][j]=='空':
                        boardBar += '×'
                    else:
                        boardBar += '  '
        print(boardBar)
        boardBar = ''


defaultSize = 9

if __name__ == '__main__':
    board = defineSquare(defaultSize)
    realBoard = defineSquare(defaultSize)

    notBeenPlaced = {
        1: list(range(1, defaultSize+1)),
        2: list(range(1, defaultSize+1))
    }

    pos = [0, 0]

    nowPlayer = 1
    while True:
        if sys.platform == 'win32':
            os.system("cls")
        elif sys.platform == 'linux':
            os.system("clear")

        notBeenPlaced[nowPlayer].sort()

        printBoard(realBoard, board, pos)

        if len(notBeenPlaced[nowPlayer]) == 0:
            print("Player {} :You Lost!".format(nowPlayer))
            break
        print("当前玩家： Player {} \n你现在持有的数字： {} \n选定坐标并写下数字，可用 [WASD]或[↑←↓→] 移动指针\n".format(
            nowPlayer, notBeenPlaced[nowPlayer]))

        inputtedChar = getch()

        if inputtedChar == b'\x1b':
            break
            # 按下Esc退出游戏
        elif inputtedChar == b'\xe0':
            inputtedChar = getch()
            if inputtedChar == b'H':
                #上
                pos[0]-=1
            elif inputtedChar == b'K':
                #左
                pos[1]-=1
            elif inputtedChar == b'P':
                #下
                pos[0]+=1
            elif inputtedChar == b'M':
                #右
                pos[1]+=1
        elif inputtedChar in (b'W',b'w'):
            #上
            pos[0]-=1
        elif inputtedChar in (b'a',b'A'):
            #左
            pos[1]-=1
        elif inputtedChar in (b's',b'S'):
            #下
            pos[0]+=1
        elif inputtedChar in (b'd',b'D'):
            #右
            pos[1]+=1
        elif int(inputtedChar) in tuple(range(10)):
            placeNum = int(inputtedChar)
        
        
        
            if placeNum in notBeenPlaced[nowPlayer]:
                notBeenPlaced[nowPlayer].pop(
                    notBeenPlaced[nowPlayer].index(placeNum))
            else:
                print("您手中无此棋子。")
                continue
            square = couldPlace(board, pos, placeNum)
            if not square:
                print("data: "+str(pos)+' - '+str(placeNum)+' ingored')
                # 输入数据无效;
                notBeenPlaced[nowPlayer].append(placeNum)
                input()
                continue
            else:
                board = square
                realBoard[pos[0]][pos[1]] = placeNum
            nowPlayer += 1
            if nowPlayer >= 3:
                nowPlayer = 1


input()
