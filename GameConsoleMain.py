# -*- coding: utf-8 -*-

# 生命灵动，当用激情跃起奋发之力

# 奇偶数阵

# 学海无涯 应用爱意徜徉
# 在生命的起源寻找灵魂的慰藉




import os


def defineSquare(size: int = 9):
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


def printBoard(realBoard: list):
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
                boardBar += '□'
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

    nowPlayer = 1
    while True:
        os.system("cls")
        printBoard(realBoard)
        try:
            pos = input("当前玩家： Player"+nowPlayer+"\n输入坐标及你的数字，用 空格 隔开。\n")
        except:
            continue
        pos, placeNum = ([int(pos.split(' ')[0]), int(
            pos.split(' ')[1])], int(pos.split(' ')[2]))
        if placeNum in notBeenPlaced[nowPlayer]:
            notBeenPlaced[nowPlayer].pop(
                notBeenPlaced[nowPlayer].index(placeNum))
        else:
            print("ERROR! 此棋子已被放置")
        square = couldPlace(board, pos, placeNum)
        if not square:
            print("data: "+str(pos)+' - '+str(placeNum)+' ingored')
            # 输入数据无效;
            input()
            continue
        else:
            board = square
            realBoard[pos[0]][pos[1]] = placeNum
        nowPlayer += 1
        if nowPlayer >= 3:
            nowPlayer = 1


input()
