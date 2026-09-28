import sys
import pygame
import numpy as np

#grid map
cellmap = np.zeros((8,8), dtype=int)
for row in range(cellmap.shape[0]):
    for col in range(cellmap.shape[1]):
        if row%2 == col%2:
            cellmap[row][col] = 1

#pieces map
piecesmap = np.zeros((8,8), dtype=str)
for row in range(piecesmap.shape[0]):
    for col in range(piecesmap.shape[1]):
        if row in (0,1,2) and row%2 !=col%2:
            piecesmap[row][col] = 'b'
        elif row in (5,6,7) and row%2 != col%2:
            piecesmap[row][col] = 'w'

#variables related to the window
_VARS = {'surf': False, 'gridWH':400,'gridOrigin':(100,140), 'gridCells':cellmap.shape[0], 'lineWidth':2}

#constants
SCREENSIZE = WIDTH, HEIGHT = 600,600
LIGHTCOLOR = (219, 184, 108)
DARKCOLOR = (69, 36, 20)
CELLDIMX=CELLDIMY= float(_VARS['gridWH']/_VARS['gridCells']) #cell dimensions

#this allows me to get which row and column the click was on
def getRowCol():
    ev = pygame.event.get()
    for event in ev:
        #if mouse button clicked
        if event.type == pygame.MOUSEBUTTONUP:
            #this gets the position of the click
            x,y = pygame.mouse.get_pos()
            #checks if the click was in the grid
            if _VARS['gridWH']<=x or x <=_VARS['gridOrigin'][0] or _VARS['gridWH']<=y or y<=_VARS['gridOrigin'][1]: 
                return False
            else:
                #if not calculates which row based on the formula that gave us x and y
                row = (x- _VARS['gridOrigin'][0] - _VARS['lineWidth']/2) //CELLDIMX
                col = (y - _VARS['gridOrigin'][1] - _VARS['lineWidth']/2) //CELLDIMY
                return (row,col)


def placePieces():

    #drawing the pieces
    def drawPieces(origin, radius, color):
        pygame.draw.circle(_VARS['surf'], center=origin, radius=radius, color=color)

    #placing them appropriately
    for row in range(_VARS['gridCells']):
        for col in range(_VARS['gridCells']):
            #computing the center of the squares.
            x = _VARS['gridOrigin'][0] + (CELLDIMX*row)+_VARS['lineWidth']/2 + CELLDIMX/2
            y = _VARS['gridOrigin'][1] + (CELLDIMY*col)+_VARS['lineWidth']/2 + CELLDIMY/2
            center = (x,y)
        #checking where the white and black pieces are
            if piecesmap[col][row] == 'w':
                drawPieces( center ,CELLDIMX/2.5, 'white')
            elif piecesmap[col][row] == 'b':
                drawPieces( center ,CELLDIMX/2.5, 'black')    
    

def drawBoard():
    
    def placeCells(): #the function places cell on the grid

        for row in range(_VARS['gridCells']):
            for col in range(_VARS['gridCells']):
                #compute x and y
                x = _VARS['gridOrigin'][0] + (CELLDIMX*row)+_VARS['lineWidth']/2
                y = _VARS['gridOrigin'][1] + (CELLDIMY*col)+_VARS['lineWidth']/2

                #alternating colors
                if cellmap[row][col] == 1:
                    color = LIGHTCOLOR
                else: color = DARKCOLOR
                drawSquareCell(x,y, CELLDIMX,CELLDIMY,color)

    def drawSquareCell(x,y,dimx,dimy,color): # the functions draws said cells         
        pygame.draw.rect(_VARS['surf'], color, (x,y,dimx,dimy))

    def drawSquareGrid(origin, gridWH, cells): #this one draws the grid

        #size of the grid
        CONTAINER_SIZE = gridWH
        #act as the pivot, allowing us to move the grid
        cont_x, cont_y = origin
        
        #draw the border
        #top
        pygame.draw.line(_VARS['surf'],'black', (cont_x, cont_y), (CONTAINER_SIZE+cont_x, cont_y), _VARS['lineWidth'])
        #bottom
        pygame.draw.line(_VARS['surf'],'black',(cont_x, CONTAINER_SIZE+cont_y),(CONTAINER_SIZE+cont_x, CONTAINER_SIZE+cont_y) ,  _VARS['lineWidth'])
        #left
        pygame.draw.line(_VARS['surf'],'black', (cont_x, cont_y), (cont_x,CONTAINER_SIZE+ cont_y),  _VARS['lineWidth'])
        #right
        pygame.draw.line(_VARS['surf'],'black', (CONTAINER_SIZE+cont_x, cont_y), (CONTAINER_SIZE+cont_x, CONTAINER_SIZE+cont_y),  _VARS['lineWidth'])

        cellSize=CONTAINER_SIZE//cells

        #actually drawing the grid
        for x in range(cells):
            #vertical
            pygame.draw.line(_VARS['surf'], 'black', (cont_x+(cellSize*x),cont_y), (cont_x+(cellSize*x),CONTAINER_SIZE+cont_y), _VARS['lineWidth'])
            #horizontal
            pygame.draw.line(_VARS['surf'], 'black', (cont_x,cont_y+(cellSize*x)), (CONTAINER_SIZE+cont_x,cont_y+(cellSize*x)), _VARS['lineWidth'])
    
    drawSquareGrid(_VARS['gridOrigin'],_VARS['gridWH'], _VARS['gridCells'])
    placeCells()


#main game loop
def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running = False
        _VARS['surf'].fill('grey')
        drawBoard()
        placePieces()
        pygame.display.update()
        


if __name__ == '__main__':
    main()