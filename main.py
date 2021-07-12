import pygame
from math import ceil, sqrt
from time import sleep
open = list()
closed = list()


class Node:
    def __init__(self, row, col):
        self.color = (0, 0, 0)
        self.row = row
        self.col = col
        self.width = self.height = 28
        self.isObstacle = False
        self.isStartNode = False
        self.isEndNode = False
        self.g_cost = int()
        self.h_cost = int()
        self.f_cost = int()

    def get_f_cost(self):
        self.g_cost = 0
        self.h_cost = ceil(sqrt((self.row - endNode.row)**2 + (self.col - endNode.col)**2))*10
        print(self.h_cost)
        self.f_cost = self.g_cost + self.h_cost


board = [[Node(row, col) for row in range(0, 20)] for col in range(0, 20)]


def drawBoard():
    for row in board:
        for node in row:
            pygame.draw.rect(screen, node.color, pygame.Rect(node.row * 30 + 2, node.col * 30 + 2, 28, 28))
    pygame.display.flip()


def aStar(display, current=False):
    lowest = 99999999
    try:
        current.color = (0, 255, 0)
    except:
        print("xd")
    for node in open:
        if node.f_cost < lowest:
            lowest = node.f_cost
            current = node
    current.color = (0,100,0)
    drawBoard()
    open.remove(current)
    closed.append(current)
    if current == endNode:
        return current
        # TODO: COLOR GOOD PATH!
    neighbours = appendNeighbours(current.row, current.col)
    for neighbour in neighbours:
        if neighbour not in open:
            open.append(neighbour)
    return aStar(display, current)


def appendNeighbours(col, row):
    drawBoard()
    sleep(0.05)
    g_cost = board[row][col].g_cost
    neighbours = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                pass
            else:
                if col+j != -1 and col+j != 20 and row+i != -1 and row+i != 20:
                    try:
                        if board[row + i][col + j].isObstacle is False and board[row + i][col + j] not in closed:
                            neighbours.append(board[row + i][col + j])
                            board[row + i][col + j].get_f_cost()
                            board[row + i][col + j].color = (0, 0, 255)
                            if i == 0 or j == 0:
                                board[row + i][col + j].g_cost = g_cost + 10
                            else:
                                board[row + i][col + j].g_cost = g_cost + 14
                    except:
                        print(col+i, row+i)
    return neighbours


pygame.init()
screen = pygame.display.set_mode((600, 600))
running = True
screen.fill((84, 84, 84))
startNode = board[0][0]
endNode = board[19][19]
gameStarted = False
while running:
    while not gameStarted:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gameStarted = True
            if pygame.mouse.get_pressed()[0]:
                try:
                    col = ceil(pygame.mouse.get_pos()[0] / 30)
                    row = ceil(pygame.mouse.get_pos()[1] / 30)
                    board[row - 1][col - 1].isObstacle = True
                    board[row - 1][col - 1].isStartNode = False
                    board[row - 1][col - 1].isEndNode = False
                    board[row - 1][col - 1].color = (255, 0, 0)
                except AttributeError:
                    pass
            elif pygame.mouse.get_pressed()[1]:
                try:
                    col = ceil(pygame.mouse.get_pos()[0] / 30)
                    row = ceil(pygame.mouse.get_pos()[1] / 30)
                    if endNode is not board[row - 1][col - 1]:
                        startNode.isStartNode = False
                        startNode.color = (0, 0, 0)
                        board[row - 1][col - 1].isStartNode = True
                        board[row - 1][col - 1].color = (0, 255, 0)
                        startNode = board[row - 1][col - 1]
                except AttributeError:
                    pass
            elif pygame.mouse.get_pressed()[2]:
                try:
                    col = ceil(pygame.mouse.get_pos()[0] / 30)
                    row = ceil(pygame.mouse.get_pos()[1] / 30)
                    if startNode is not board[row - 1][col - 1]:
                        endNode.isEndNode = False
                        endNode.color = (0, 0, 0)
                        board[row - 1][col - 1].isEndNode = True
                        board[row - 1][col - 1].color = (0, 0, 255)
                        endNode = board[row - 1][col - 1]
                except AttributeError:
                    pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameStarted = True
        drawBoard()
    if running:
        print(startNode.row, startNode.col)
        open.append(startNode)
        x = aStar(True)
        drawBoard()
        while gameStarted:
            print(endNode, x)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameStarted = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        board = [[Node(row, col) for row in range(0, 20)] for col in range(0, 20)]
                        startNode = board[0][0]
                        endNode = board[0][0]
                        gameStarted = False
