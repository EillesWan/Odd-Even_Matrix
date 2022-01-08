import sys
import time
import threading
from typing import Text, Tuple
import pygame

from oemsup.threadOpera import newThread

pygame.init() # 初始化pygame

# 初始设置
screen = pygame.display.set_mode((600,800),pygame.RESIZABLE) # Pygame窗口
pygame.display.set_caption("金羿 - 奇偶数阵") # 标题


radius = 20 # 半径



screen.fill((255,255,255))
screen.blit(pygame.image.load('./resources/RyounGril.png'),(0,0))
screen.blit(pygame.font.SysFont('DengXian',50).render("请等待程序加载……",True,(0,0,0)),(0,601))

pygame.display.update()




#time.sleep(3)




# 计算用函数

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






# 显示用函数



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





def drawSquare(surface: pygame.Surface, color:tuple, position:tuple, size:tuple):
    '''在`surface`上绘制矩形
    :param surface pygame Surface对象
    :param color 颜色数组(RGB)或(RGBA)
    :param position 矩形左上角的位置
    :param size 矩形大小(以像素为准)
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


def drawHollowSquare(surface: pygame.Surface, color:tuple, position:tuple, size:tuple):
    '''在`surface`上绘制空心矩形
    :param surface pygame Surface对象
    :param color 颜色数组(RGB)或(RGBA)
    :param position 矩形左上角的位置
    :param size 矩形大小(以像素为准)
    '''
    
    pygame.draw.aalines(
        surface,
        color,
        True,
        (
            (
                int(position[0]),
                int(position[1])
            ),
            (
                int(position[0]+size[0]),
                int(position[1])
            ),
            (
                int(position[0]+size[0]),
                int(position[1]+size[1])
            ),
            (
                int(position[0]),
                int(position[1]+size[1])
            ),
            
        )
    )




def drawText(surface: pygame.Surface, text: str, color: tuple, position: tuple, size, isBold=False, isItalic=False, font='DengXian', isAntialias=True, bg=None):
    '''在`surface`上写下`text`
    :param surface pygame Surface对象
    :param text 显示的文字
    :param color 颜色数组(RGB)或(RGBA)
    :param position 文字左上角的位置
    :param size 文字字号(以像素为准)
    :param isBold 是否加粗 默认为 `False`
    :param isItalic 是否斜体 默认为 `False`
    :param font 字体 默认为 `DengXian`
    :param isAntialias 是否使用平滑字体 默认为 `True`
    :param bg 背景颜色 默认为 `None`，即无背景色
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



defaultBlue = (0,137,242)
defaultRed = (255,52,50)
defaultPurple = (171,112,255)
defaultGreen = (0,255,33)
defaultWhite = (242,244,246)
defaultBlack = (18,17,16)



def drawBoard(surface: pygame.Surface, realBoard: list, sourceBoard: list, select: list, check: list):


    posX, posY = screen.get_width()/2-(screen.get_height()*49/160),screen.get_height()*11/160

    def drawSquareSmall(color):
        drawSquare(surface, color,
                   (posX + (screen.get_height() * 197 / 2880) * j,
                    posY + (screen.get_height() * 197 / 2880) * i),
                   (screen.get_height() * 47 / 720,
                    screen.get_height() * 47 / 720)
                   )
    
    def drawTextSmall(text):
        drawText(
            surface,
            text,
            defaultWhite,
            (
                posX+(screen.get_height()*197/2880)*j,
                posY + (screen.get_height()*197/2880)*i
            ),
            screen.get_height()*47/720
        )

    
    def drawHollowSquareSmall(color):
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
                drawSquareSmall(defaultBlue)
                drawTextSmall(str(realBoard[i][j]))
            else:
                # 是否被占格？
                if sourceBoard[i][j]==1:
                    drawSquareSmall(defaultGreen)
                elif sourceBoard[i][j]==2:
                    drawSquareSmall(defaultPurple)
                elif sourceBoard[i][j]=='空':
                    drawSquareSmall(defaultRed)
                else:
                    drawSquareSmall(defaultBlue)
            
            if i == check[0] and j == check[1]:
                # 是否被指针按下确认？
                drawHollowSquareSmall(defaultBlack)

            if i == select[0] and j == select[1]:
                # 是否被指针选中？
                drawHollowSquareSmall(defaultWhite)
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
            



print('Load Over')


defaultSize = 9






def __main__():


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

    selected = (0,0)
    '''当前指针所确认的方格'''

    nowPlayer = 1
    '''当前的玩家'''


    # 游戏循环
    while True:
        for event in pygame.event.get():  # 遍历事件
            if event.type == pygame.QUIT:  # 退出事件
                print("EXIT")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 按下鼠标？

                if event.button == 1:

                    mousePosX, mousePoxY = event.pos

                    posX = mousePosX-(screen.get_width()/2-(screen.get_height()*49/160))

                    posY = mousePoxY-screen.get_height()*11/160

                    if (posX >= 0 and posX <= screen.get_height()*49/80) and (posY >= 0 and posY <= screen.get_height()*49/80):
                        #鼠标在棋盘范围内
                        selected = (
                            int(posY/(screen.get_height()*197/2880)),
                            int(posX/(screen.get_height()*197/2880)),
                        )
                        
                        
                    
                    del posX,posY,mousePosX,mousePoxY
            elif event.type == pygame.MOUSEMOTION:
                mousePosX, mousePoxY = event.pos

                posX = mousePosX-(screen.get_width()/2-(screen.get_height()*49/160))

                posY = mousePoxY-screen.get_height()*11/160

                if (posX >= 0 and posX <= screen.get_height()*49/80) and (posY >= 0 and posY <= screen.get_height()*49/80):
                    #鼠标在棋盘范围内
                    pos = (
                        int(posY/(screen.get_height()*197/2880)),
                        int(posX/(screen.get_height()*197/2880)),
                    )
                
            elif event.type == pygame.KEYDOWN:
                print(notBeenPlaced[nowPlayer])
                if event.key == pygame.K_ESCAPE:
                    print("EXIT")
                    pygame.quit()
                    sys.exit()
                if event.key in tuple(range(48,58))+tuple(range(1073741913,1073741923)):
                    print("KEY",event.key)
                    if event.key in tuple(range(48,58)):
                        placeNum = event.key - 48
                    if event.key in tuple(range(1073741913,1073741923)):
                        placeNum = (event.key - 1073741912)%10
            
                    if placeNum in notBeenPlaced[nowPlayer]:
                        notBeenPlaced[nowPlayer].pop(
                            notBeenPlaced[nowPlayer].index(placeNum))
                    else:
                        print("您手中无此棋子。")
                        continue
                    square = couldPlace(sourceBoard, selected, placeNum)
                    if not square:
                        print("data: "+str(selected)+' - '+str(placeNum)+' ingored')
                        # 输入数据无效;
                        notBeenPlaced[nowPlayer].append(placeNum)
                        continue
                    else:
                        sourceBoard = square
                        realBoard[selected[0]][selected[1]] = placeNum
                    nowPlayer += 1
                    if nowPlayer >= 3:
                        nowPlayer = 1
            

            #print(str(event))
        
        screen.fill(defaultBlack)
        
        


        drawText(screen,'就绪',defaultWhite,
                (int(screen.get_width()/2-50), 0),
                int(screen.get_height()/16)
                )

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

        

        pygame.display.update()  # 刷新屏幕



if __name__ == '__main__':
    __main__()