# -*- coding: utf-8 -*-

# 生命灵动，当用激情跃起奋发之力

# 奇偶数阵

# 学海无涯 应用爱意徜徉
# 在生命的起源寻找灵魂的慰藉

'''
Copyright 2022 Eilles Wan (金羿)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''






from copy import deepcopy as dc
from email.contentmanager import raw_data_manager
from email.policy import default
import sys
import pygame
from typing import Union


pygame.init() # 初始化pygame

# 初始设置
screen = pygame.display.set_mode((600,800),pygame.RESIZABLE) # Pygame窗口
pygame.display.set_caption("金羿 - 奇偶数阵") # 标题


#radius = 20 # 半径



screen.fill((255,255,255))
screen.blit(pygame.image.load('./resources/RyounGril.png'),(0,0))
screen.blit(pygame.font.SysFont('DengXian',50).render("请等待程序加载……",True,(0,0,0)),(0,601))

pygame.display.update()










def defineSquare(size: int = 9) -> list:
    # 建立空的棋盘
    square = []
    for i in range(size):
        square.append([])
        for j in range(size):
            square[i].append(None)
    return square




# 游戏运行数据



BLUE = (0,137,242)
RED = (255,52,50)
PURPLE = (171,112,255)
GREEN = (0,255,33)
WHITE = (242,244,246)
BLACK = (18,17,16)

defaultSize = 9
'''默认棋盘大小'''













# 计算用函数



def isEven(n: int) -> int:
    if n % 2 == 0:
        return 2
    else:
        return 1


def couldPlace(square: list, pos: tuple, num: int) -> Union[bool, list]:
    '''返回是否能够放置棋子，若不能，则返回`False`，若能够，则返回放置后的源盘

    Parameters
    --------
    square: :class:`list`
        当前的源盘（SourceBoard）
    pos: :class:`tuple`
        需要判定的位置
    num: :class:`int`
        需要判定的数字'''
    # print(pos)
    num = isEven(num)
    
    if square[pos[0]][pos[1]] and square[pos[0]][pos[1]] != num:
        return False

    if num == 1:
        square[pos[0]][pos[1]] = '奇'
    elif num == 2:
        square[pos[0]][pos[1]] = '偶'

    for i in range(len(square)):
        # 遍历行
        #print(str(i)+','+str(pos[1]))
        if square[i][pos[1]] and square[i][pos[1]] != num:
            square[i][pos[1]] = '空'
        else:
            square[i][pos[1]] = num
    for j in range(len(square[pos[0]])):
        # 遍历对应列
        #print(str(pos[0])+' '+str(j))
        if square[pos[0]][j] and square[pos[0]][j] != num:
            square[pos[0]][j] = '空'
        else:
            square[pos[0]][j] = num
    i = pos[0]
    j1 = pos[1]
    j2 = pos[1]
    while i >= 0:
        # 遍历上半部分斜线
        #print(str(i)+':'+str(j1))
        #print(str(i)+':'+str(j2))
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
        #print(str(i)+'`'+str(j1))
        #print(str(i)+'`'+str(j2))
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














# 显示用函数



def printBoard(realBoard: list, sourceBoard: list, select: list) -> None:
    '''在控制台打印棋盘

    Parameters
    ----------
    realBoard: :class:`list`
        显示出来的棋盘
    sourceBoard: :class:`list`
        解析用的棋盘
    select: :class:`list`
        当前选中的方格
    '''
    boardBar = '  '
    for i in range(len(realBoard)):
        boardBar += str(i)+'|'
    #print(boardBar)
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
        #print(boardBar)
        boardBar = ''






def drawSquare(surface: pygame.Surface, color:tuple, position:tuple, size:tuple) -> None:
    '''在`surface`上绘制矩形

    Parameter
    ---------
    surface: :class:`pygame.Surface`
        pygame Surface对象
    color: :class:`tuple`
        颜色数组(RGB)或(RGBA)
    position: :class:`tuple`
        矩形左上角的位置
    size: :class:`tuple`
        矩形大小(以像素为准)
    '''
    pygame.draw.rect(
        surface,
        color,
        pygame.rect.Rect(
            int(position[0]),
            int(position[1]),
            int(size[0]),
            int(size[1])
        )
    )





def drawHollowSquare(surface: pygame.Surface, color:tuple, position:tuple, size:tuple, width:int = 1) -> None:
    '''在`surface`上绘制空心矩形

    Parameter
    ---------
    surface: `pygame.Surface`
        pygame Surface对象
    color: `tuple`
        颜色数组(RGB)或(RGBA)
    position: `tuple`
        矩形左上角的位置
    size: `tuple`
        矩形大小(以像素为准)
    width: `int`
        矩形边宽度(以像素为准)
    '''

    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(int(position[0]), int(position[1]), size[0], size[1]),
        width
    )





def drawText(surface: pygame.Surface, text: str, color: tuple, position: tuple, size: int, isBold=False, isItalic=False, font='DengXian', isAntialias=True, bg=None) -> None:
    '''在`surface`上写下`text`

    Parameter
    --------
    surface: `pygame.Surface`
        pygame Surface对象
    text: `str`
        显示的文字
    color: `tuple`
        颜色数组(RGB)或(RGBA)
    position: `tuple`
        文字左上角的位置
    size: int
        文字字号(以像素为准)
    isBold: `bool`
        是否加粗 默认为 `False`
    isItalic: `bool`
        是否斜体 默认为 `False`
    font: `str`
        字体 默认为 `DengXian`
    isAntialias: `bool`
        是否使用平滑字体 默认为 `True`
    bg: `tuple`
        背景颜色 默认为 `None`，即无背景色
    '''
    surface.blit(
        pygame.font.SysFont(
            font,
            int(size),
            isBold,
            isItalic
        ).render(
            text,
            isAntialias,
            color,
            bg
        ),
        (
            int(position[0]),
            int(position[1]),
        )
    )






def drawBoard(surface: pygame.Surface, realBoard: list, sourceBoard: list, select: list, check: list) -> None:
    '''在`surface`绘制棋盘

    Parameter
    ---------
    surface: `pygame.Surface`
        pygame Surface对象
    realBoard: `list`
        显示出来的棋盘
    sourceBoard: `list`
        解析用的棋盘
    select: `list`
        当前指针所在的的方格
    check: `list`
        按下了鼠标左键之后选中的方格
    '''

    posX, posY = screen.get_width()/2-(screen.get_height()*49/160),screen.get_height()*11/160

    def drawSquareSmall(color:tuple) -> None:
        drawSquare(surface, color,
                   (posX + (screen.get_height() * 197 / 2880) * j,
                    posY + (screen.get_height() * 197 / 2880) * i),
                   (screen.get_height() * 47 / 720,
                    screen.get_height() * 47 / 720)
                   )
    
    def drawTextSmall(text:str) -> None:
        drawText(
            surface,
            text,
            WHITE,
            (
                posX+(screen.get_height()*197/2880)*j,
                posY + (screen.get_height()*197/2880)*i
            ),
            screen.get_height()*47/720
        )

    
    def drawHollowSquareSmall(color:tuple) -> None:
        drawHollowSquare(surface, color,
                    (
                        posX + screen.get_height()*(197*j+9)/2880,
                        posY + screen.get_height()*(197*i+9)/2880,
                    ),
                    (
                        screen.get_height()*83/1440,
                        screen.get_height()*83/1440)
                    )
        # drawSquare(surface, defaultWhite,
        #            (posX + (screen.get_height() * 197 / 2880) * j,
        #             posY + (screen.get_height() * 197 / 2880) * i),
        #            (screen.get_height() * 47 / 720,
        #             screen.get_height() * 47 / 720)
        #            )

    for i in range(len(realBoard)):
        for j in range(len(realBoard)):

            if realBoard[i][j]:
            # 是否存在数字？
                drawSquareSmall(BLUE)
                drawTextSmall(str(realBoard[i][j]))
            else:
                if sourceBoard[i][j]==1:
                    drawSquareSmall(GREEN)
                elif sourceBoard[i][j]==2:
                    drawSquareSmall(PURPLE)
                elif sourceBoard[i][j]=='空':
                    drawSquareSmall(RED)
                else:
                    drawSquareSmall(BLUE)
            
            if i == check[0] and j == check[1]:
                # 是否被指针按下确认？
                drawHollowSquareSmall(BLACK)

            if i == select[0] and j == select[1]:
                # 是否被指针选中？
                drawHollowSquareSmall(WHITE)
            # 增加的调试信息
            # drawText(
            #     surface,
            #     "({},{})".format(j,i),
            #     defaultWhite,
            #     (
            #         posX + (screen.get_height()*197/2880)*j,
            #         posY + (screen.get_height()*197/2880)*i
            #     ),
            #     20
            # )
            



def drawNoticeTitle(surface: pygame.Surface,text:str,color = WHITE) -> None:
    '''在`surface`上把`text`绘制棋盘上面作为提示标题

    Parameters
    ---------
    surface: `pygame.Surface`
        pygame Surface对象
    text: `str`
        需要显示的标题
    color: `tuple`
        标题颜色
    '''
    drawText(
        surface,
        text,
        color,
            (
                int(surface.get_width()/2-len(text)*surface.get_height()/32),
                0
            ),
        int(surface.get_height()/16)
    )






def drawNumbers(surface: pygame.Surface, numberList: tuple, focus: tuple) -> None:
    '''在`surface`上绘制数字方块

    Parameters
    ---------
    surface: `pygame.Surface`
        pygame Surface对象
    numberList: `tuple`
        数字列表
    focus: `tuple`
        当前指针所在的的方格
    '''

    posX, posY = screen.get_width()/2-(screen.get_height()*49/160), screen.get_height()*121/160

    def drawSquareSmall(color:tuple,isUp:bool) -> None:
        drawSquare(surface,
                   color,
                   (
                        posX + (screen.get_height() * 197 / 2880) * (num - 1),
                        screen.get_height()*29/40 if isUp else posY
                   ),
                   (
                       screen.get_height() * 47 / 720,
                       screen.get_height() * 47 / 720)
                   )
    
    def drawTextSmall(text:str,isUp:bool) -> None:
        drawText(
            surface,
            text,
            WHITE,
            (
                posX + (screen.get_height() * 197 / 2880) * (num - 1),
                screen.get_height()*29/40 if isUp else posY
            ),
            screen.get_height() * 47 / 720
        )



    for num in numberList:
        
        drawSquareSmall(
            GREEN if isEven(num) == 1 else PURPLE,
            True if focus[1]+1 == num and focus[0] == 10 else False
            )
        drawTextSmall(str(num),True if focus[1]+1 == num and focus[0] == 10 else False)


def numberMovement(surface, posNum : list, posBoard : list) -> None:
    num = posNum[1]+1
    color = GREEN if isEven(num) == 1 else PURPLE
    
    posX, posY = screen.get_width()/2-(screen.get_height()*49/160),screen.get_height()*11/160

    startPos = (
        posX + (screen.get_height() * 197 / 2880) * posNum[1],
        posY + (screen.get_height() * 197 / 2880) * posNum[0]
    )

    endPos = (
        posX + (screen.get_height() * 197 / 2880) * posBoard[1],
        posY + (screen.get_height() * 197 / 2880) * posBoard[0]
    )

    def __drawBlock(position: tuple):
        drawSquare(surface, color,
                   position,
                   (screen.get_height() * 47 / 720,
                    screen.get_height() * 47 / 720)
                   )
        drawText(
            surface,
            str(num),
            WHITE,
            position,
            screen.get_height()*47/720
        )
    
    for i in range(int(startPos[0]),int(endPos[0])):
        for j in range(int(startPos[1]),int(endPos[1])):
            __drawBlock((i,j,))

def allNone(check:list) -> bool:
    all = True
    for x in check:
        if x:
            all = False
            break
    return all

def isGameOver(game:list, current_nums:list) -> Union[bool, None]:

    if not(current_nums):
        return None

    odd = [x for x in current_nums if x % 2 == 1]
    even = [x for x in current_nums if x % 2 == 0]
    returnValue = False

    all = []
    haveEven = [None for x in range(9)]
    for index,row in enumerate(game):
        dcrow = dc(row)
        # print(f"{index}: {row}")
        while "空" in dcrow: dcrow.remove("空")
        for x in dcrow: all.append(x)
        if 2 in dcrow:
            haveEven[index] = 2
        elif 1 in dcrow:
            haveEven[index] = 1
    
    if (1 in all) and (2 in all): return False
    # print(f"check1: {returnValue}, all: {all}")

    # 不可能放棋子+不是第一回（因为刚开始全是'空'）
    if (allNone(haveEven)) and (len(current_nums) != 9):
        returnValue = True
    elif len(odd) and len(even):
        returnValue = False

    # print(f"check2: {returnValue}, even: {haveEven}")

    all_even = False
    for x in haveEven:
        if x == 2:
            all_even = True
            break
    #全奇 + 没有奇数
    #print(f"check2: {odd}")
    if not(all_even) and not(len(odd)):
        returnValue = True
    #全偶 
    elif all_even and not(len(even)):
        returnValue = True

    # print(f"check3: {all_even}, {returnValue}")

    return returnValue

def gameRun():


    sourceBoard = defineSquare(defaultSize)
    '''存储用于解析的棋盘
        棋子：
            奇数：1
            偶数：2
        占格：
            奇数：'奇'
            偶数：'偶'
            不能填：'空'
    '''

    realBoard = defineSquare(defaultSize)
    '''存储显示出来的棋盘，即仅包含下下来的数字'''

    notBeenPlaced = {
        1: list(range(1, defaultSize+1)),
        2: list(range(1, defaultSize+1))
    }
    '''当前玩家所剩的数字'''

    pos = (0, 0)
    '''当前指针所指向的方格'''

    selected = (-1,-1)
    '''当前指针所确认的方格'''

    nowPlayer = 1
    '''当前的玩家'''

    mouseSelectedArea = (0,None)
    '''第一个值鼠标选择区域： 0无指示部分，1棋盘，2数字区域；第二个值：指针所在方格'''

    noticeTitle = ("就绪",WHITE)
    '''窗口下的大标题显示的内容'''


    # 游戏循环
    while True:

        events = pygame.event.get()
        if events:
            for event in events:  # 遍历事件
                if event.type == pygame.QUIT:  # 退出事件
                    # print("EXIT")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 按下鼠标？

                    if event.button == 1:

                        mousePosX, mousePosY = event.pos

                        posX = mousePosX-(screen.get_width()/2-(screen.get_height()*49/160))

                        posY = mousePosY-screen.get_height()*11/160

                        selected = (
                                int(posY/(screen.get_height()*197/2880)+1)-1,
                                int(posX/(screen.get_height()*197/2880)+1)-1,
                            )
                        
                        if (selected[1] >= 0 and selected[1] < defaultSize):
                            if (selected[0] >= 0 and selected[0] < defaultSize):
                                #鼠标在棋盘范围内
                                if mouseSelectedArea[0] == 2:
                                    placeNum = mouseSelectedArea[1][1] + 1
                                    
                                    if placeNum in notBeenPlaced[nowPlayer]:
                                        notBeenPlaced[nowPlayer].pop(
                                            notBeenPlaced[nowPlayer].index(placeNum)
                                        )
                                    else:
                                        # print("您手中无此棋子。")
                                        noticeTitle = ("您手中无此数字",RED)
                                        continue
                                    square = couldPlace(sourceBoard, selected, placeNum)
                                    if not square:
                                        # print("data: "+str(selected)+' - '+str(placeNum)+' ingored')
                                        # 输入数据无效;
                                        notBeenPlaced[nowPlayer].append(placeNum)
                                        notBeenPlaced[nowPlayer].sort()
                                        noticeTitle = ("棋子奇偶性不符合要求", RED)
                                        continue
                                    else:
                                        sourceBoard = square
                                        realBoard[selected[0]][selected[1]] = placeNum
                                    nowPlayer += 1
                                    if nowPlayer >= 3:
                                        nowPlayer = 1

                                    numberMovement(screen,mouseSelectedArea[1],selected)
                                    mouseSelectedArea = (0,None)
                                else:
                                    mouseSelectedArea = (1,selected)
                                noticeTitle = ("选中棋盘({},{})".format(selected[0],selected[1]),BLUE)
                            elif selected[0] == 10:
                                #鼠标在数字范围内
                                if mouseSelectedArea[0] == 1:
                                    placeNum = selected[1] + 1
                                    
                                    if placeNum in notBeenPlaced[nowPlayer]:
                                        notBeenPlaced[nowPlayer].pop(
                                            notBeenPlaced[nowPlayer].index(placeNum)
                                        )
                                    else:
                                        # print("您手中无此棋子。")
                                        noticeTitle = ("您手中无此数字",RED)
                                        continue
                                    square = couldPlace(sourceBoard, mouseSelectedArea[1], placeNum)
                                    if not square:
                                        # print("data: "+str(mouseSelectedArea[1])+' - '+str(placeNum)+' ingored')
                                        # 输入数据无效;
                                        notBeenPlaced[nowPlayer].append(placeNum)
                                        notBeenPlaced[nowPlayer].sort()
                                        continue
                                    else:
                                        sourceBoard = square
                                        realBoard[mouseSelectedArea[1][0]][mouseSelectedArea[1][1]] = placeNum
                                    nowPlayer += 1
                                    if nowPlayer >= 3:
                                        nowPlayer = 1

                                    numberMovement(screen,selected,mouseSelectedArea[1])
                                    mouseSelectedArea = (0,None)
                                else:
                                    mouseSelectedArea = (2,selected)

                                if selected[1] % 2 == 0:
                                    noticeTitle = ("选中数字{}".format(selected[1]+1),GREEN)
                                else:
                                    noticeTitle = ("选中数字{}".format(selected[1]+1),PURPLE)
                            else:
                                #鼠标啥范围都不在
                                mouseSelectedArea = (0,None)
                                noticeTitle = ("就绪",WHITE)

                        else:
                            noticeTitle = ("就绪", WHITE)
                            
                        
                        del posX,posY,mousePosX,mousePosY
                elif event.type == pygame.MOUSEMOTION:

                    posX = event.pos[0]-(screen.get_width()/2-(screen.get_height()*49/160))

                    posY = event.pos[1]-screen.get_height()*11/160

                    pos = (
                        int(posY/(screen.get_height()*197/2880)+1)-1,
                        int(posX/(screen.get_height()*197/2880)+1)-1,
                        )
                    
                    
                elif event.type == pygame.KEYDOWN:
                    
                    #print(notBeenPlaced[nowPlayer])
                    if event.key == pygame.K_ESCAPE:
                        # print("EXIT")
                        pygame.quit()
                        sys.exit()
                    if event.key in tuple(range(48,58))+tuple(range(1073741913,1073741923)):
                        # 按下数字键
                        if selected[0] in tuple(range(defaultSize)) and selected[1] in tuple(range(defaultSize)):
                            #指针选中
                            if not realBoard[selected[0]][selected[1]]:
                                #此位置没东西
                                if event.key in tuple(range(48,58)):
                                    placeNum = event.key - 48
                                if event.key in tuple(range(1073741913,1073741923)):
                                    placeNum = (event.key - 1073741912)%10
                        
                                if placeNum in notBeenPlaced[nowPlayer]:
                                    notBeenPlaced[nowPlayer].pop(
                                        notBeenPlaced[nowPlayer].index(placeNum)
                                    )
                                else:
                                    #print("您手中无此棋子。")
                                    noticeTitle = ("您手中无此数字", RED)
                                    continue
                                square = couldPlace(sourceBoard, selected, placeNum)
                                if not square:
                                    # print("data: "+str(selected)+' - '+str(placeNum)+' ignored')
                                    # 输入数据无效;
                                    notBeenPlaced[nowPlayer].append(placeNum)
                                    notBeenPlaced[nowPlayer].sort()
                                    noticeTitle = ("棋子奇偶性不符合要求", RED)
                                    continue
                                else:
                                    sourceBoard = square
                                    realBoard[selected[0]][selected[1]] = placeNum
                                nowPlayer += 1
                                if nowPlayer >= 3:
                                    nowPlayer = 1
                            else:
                                noticeTitle = ("此处已有数字", RED)
                        else:
                            noticeTitle = ("未选中棋盘", RED)

            
            screen.fill(BLACK)

            drawSquare(screen, (0, 161, 231),
                    (screen.get_width()/2-(screen.get_height()*5/16), screen.get_height()/16),
                    (screen.get_height()*5/8, screen.get_height()*5/8)
                    )

            drawSquare(screen, (38, 226, 255),
                    (screen.get_width()/2-(screen.get_height()*99/320),
                        screen.get_height()/16+screen.get_height()/320),
                    (screen.get_height()*99/160, screen.get_height()*99/160)
                    )
            
            drawBoard(screen,realBoard,sourceBoard,pos,selected)

            drawNumbers(screen,notBeenPlaced[nowPlayer],pos)

            drawText(screen,
                     f"当前玩家:{nowPlayer}",
                     BLACK,
                     (screen.get_width()/2-(screen.get_height()*49/160),
                      screen.get_height()*475/576),
                     int(screen.get_height()/16),
                     bg=WHITE
                     )
            
            check = isGameOver(sourceBoard, notBeenPlaced[nowPlayer])
            if check == None:
                noticeTitle = (f"平局！无子可走！", RED)
                return 'balance'
            elif check:
                if(nowPlayer == 1):
                    win_player = 2
                else:
                    win_player = 1
                # print(f"玩家{win_player}获胜！")
                noticeTitle = (f"玩家{win_player}获胜！", RED)
                return win_player
                
            drawNoticeTitle(screen,noticeTitle[0],noticeTitle[1])

            pygame.display.update()  # 刷新屏幕

            #pygame.time.wait(1000)
        # 每帧运行
    #跳出循环运行




def mainWindow():
    pass









def __main__():
    gameRun()


    



if __name__ == '__main__':
    __main__()