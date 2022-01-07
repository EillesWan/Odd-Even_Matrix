import sys
import time
import threading
import pygame

from oemsup.threadOpera import newThread

pygame.init() # 初始化pygame

# 初始设置
screen = pygame.display.set_mode((600,800)) # Pygame窗口
pygame.display.set_caption("金羿 - 奇偶数阵") # 标题


radius = 20 # 半径



screen.fill((255,255,255))
screen.blit(pygame.image.load('./resources/RyounGril.png'),(0,0))
screen.blit(pygame.font.SysFont('微软雅黑',120).render("请等待程序加载……",True,(0,0,0)),(0,601))

pygame.display.update()











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


print('Load Over')



# 游戏循环
while True:
    for event in pygame.event.get():  # 遍历事件
        if event.type == pygame.QUIT:  # 退出事件
            pygame.quit()
            sys.exit()
    screen.fill((0,0,0))
    
    #screen.blit(pygame.font.Font('./resources/HarmonyOS_Sans_SC_Regular.ttf',50).render("就绪",True,(255,255,255)),(0,0))
    
    screen.blit(pygame.font.SysFont('DengXian',50).render("就绪",True,(255,255,255)),(0,0))
    pygame.display.update()  # 刷新屏幕
