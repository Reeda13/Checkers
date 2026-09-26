import sys
import pygame
import numpy as np

#constants
SCREENSIZE = WIDTH, HEIGHT = 600,600
LIGHTCOLOR = (219, 184, 108)
DARKCOLOR = (69, 36, 20)

#grid map
cellmap = np.zeros((8,8), dtype=int)
for row in range(cellmap.shape[0]):
    for col in range(cellmap.shape[1]):
        if row%2 == col%2:
            cellmap[row][col] = 1

_VARS = {'surf': False, 'gridWH':400,'gridOrigin':(100,140), 'gridCells':cellmap.shape[0], 'lineWidth':2}

#main game loop
def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    while True:
        checkEvents()
        _VARS['surf'].fill('grey')
        drawBoard()
        pygame.display.update()

def drawBoard():
    
    def placeCells(): #the function places cell on the grid
    #cell dimensions
        celldimx=celldimy=_VARS['gridWH']/_VARS['gridCells']

        for row in range(_VARS['gridCells']):
            for col in range(_VARS['gridCells']):
                if cellmap[row][col] == 1:
                    color = DARKCOLOR
                else: color = LIGHTCOLOR
                drawSquareCell(_VARS['gridOrigin'][0] + (celldimx*row)+_VARS['lineWidth']/2, _VARS['gridOrigin'][1] + (celldimy*col)+_VARS['lineWidth']/2, celldimx,celldimy,color)
                
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

#quit the window
def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()