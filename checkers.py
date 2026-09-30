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
piecesmap[3][6] = 'w'
piecesmap[4][3] = 'b'

#variables related to the window
_VARS = {'surf': False, 'gridWH':400,'gridOrigin':(100,140), 'gridCells':cellmap.shape[0], 'lineWidth':2}

#constants
SCREENSIZE = WIDTH, HEIGHT = 600,600
LIGHTCOLOR = (219, 184, 108)
DARKCOLOR = (69, 36, 20)
HIGHLIGHT =(0,255,0,100)
CELLDIMX=CELLDIMY= float(_VARS['gridWH']/_VARS['gridCells']) #cell dimensions

#this allows me to get which row and column the click was on
def getRowCol(pos):
    x,y = pos
    #checks if the click was in the grid
    if _VARS['gridWH']+_VARS['gridOrigin'][0] <=x or x <=_VARS['gridOrigin'][0] or _VARS['gridWH']+_VARS['gridOrigin'][1] <=y or y<=_VARS['gridOrigin'][1]: 
        return False
    else:
        #if not calculates which row based on the formula that gave us x and y
        row = (x- _VARS['gridOrigin'][0] - _VARS['lineWidth']/2) //CELLDIMX
        col = (y - _VARS['gridOrigin'][1] - _VARS['lineWidth']/2) //CELLDIMY
        return row,col

#checks if there is a piece and gets its row and col
def containsPiece():
    pos = pygame.mouse.get_pos()
    getrowcol = getRowCol(pos)
    if getrowcol:
        col,row = getrowcol
        if piecesmap[int(row)][int(col)]:
            return row,col
        else: 
            return False

#get the coordinates
def selectedPieceCoordinates():
    selectedcell = containsPiece()
    if selectedcell:
        row,col = selectedcell
        return row,col

#draws the highlight
def drawHighlight(selected):
    #This segment makes sure to clear the highlighted cell before it
    _VARS['highlight'].fill((0,0,0,0))
    _VARS['surf'].blit(_VARS['highlight'])

    #the selected variable is a tuple storing the row and col of the cell we clicked in
    if selected:
        #extract the row and col
        row,col = selected
        #calculate the coordinates
        x = _VARS['gridOrigin'][0] + (CELLDIMX*col)+_VARS['lineWidth']/2
        y = _VARS['gridOrigin'][1] + (CELLDIMY*row)+_VARS['lineWidth']/2
        #draw the highlight
        pygame.draw.rect(_VARS['highlight'], HIGHLIGHT, (x,y,CELLDIMX,CELLDIMY))
        _VARS['surf'].blit(_VARS['highlight'])

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

def isEmpty(row,col): #Helper function to check if cell is empty
    if piecesmap[row][col] =='':
        return True
    else:
        return False

def getPossibleMoves(selected):
    possible_moves = False
    #this function computes the possible moves
    row, col = selected
    row, col = int(row), int(col)
    
    #white pieces
    if piecesmap[row][col] == 'w':
        #capturing
        
        #if a piece is at the edge with a capturable piece in sight
        if col == 0 and piecesmap[row-1][col+1]=='b' and 0<=row-2 and piecesmap[row-2][col+2] == '':
            possible_moves = [(row-2,col+2)]
        
        #if a piece is at the other edge with a capturable piece in sight
        if col == 7 and piecesmap[row-1][col-1] == 'b'and 0<=row-2 and piecesmap[row-2][col-2] == '':
            possible_moves = [(row-2, col-2)]
        
        #if piece in middle with one capture in sight
        if 0<col<7 and piecesmap[row-1][col-1] == 'b' and 0<=row-2 and 0<=col-2<=7 and piecesmap[row-2][col-2] == '' :
            possible_moves = [(row-2, col-2), (row-1, col+1)]
        
        #if piece in middle with the other capture in sight
        if 0<col<7 and piecesmap[row-1][col+1] == 'b'and 0<=row-2 and 0<=col+2<=7 and piecesmap[row-2][col+2] == '' :
            possible_moves = [(row-2, col+2), (row-1, col-1)]

        #same but for mouvement
        #if in edge
        if col==0 and row-1>=0 and isEmpty(row-1, col+1):
            possible_moves = [(row-1, col+1)]
        #if in other edge
        if col==7 and row-1>=0 and isEmpty(row-1, col-1):
            possible_moves = [(row-1, col-1)]
        #if in middle
        if 0<col<7 and row-1>=0 and isEmpty(row-1, col+1) and isEmpty(row-1, col-1):
            possible_moves = [(row-1, col+1), (row-1, col-1)]


    
    #black pieces
    if piecesmap[row][col] == 'b':
        #capturing
        #if in edge with capturable piece in range
        if col == 0 and piecesmap[row+1][col+1] == 'w' and row+2<=7 and piecesmap[row+2][col+2] == '' :
            possible_moves = [(row+2,col+2)]

        #if in other edge with capturable piece in range
        if col == 7 and piecesmap[row+1][col-1] == 'w' and row+2<=7 and piecesmap[row+2][col-2] == '' :
            possible_moves = [(row+2, col-2)]

        #if in middle with capturable piece in range
        if 0<col<7 and piecesmap[row+1][col-1] == 'w' and row+2<=7 and 0<=col-2<=7 and piecesmap[row+2][col-2] == '' :
            possible_moves = [(row+2, col-2), (row+1, col+1)]

        #if in middle with other capturable piece in range 
        if 0<col<7 and piecesmap[row+1][col+1] == 'w' and row+2<=7 and 0<=col+2<=7 and piecesmap[row+2][col+2] == '' :
            possible_moves = [(row+2, col+2), (row+1, col-1)]

        #same but for mouvement
        #if in edge
        if col==0 and isEmpty(row+1, col+1):
            possible_moves = [(row+1, col+1)]

        #if in other edge
        if col==7 and isEmpty(row+1, col-1):
            possible_moves = [(row+1, col-1)]

        #if in middle
        if 0<col<7 and row+1<=7 and  isEmpty(row+1, col+1) and isEmpty(row+1, col-1):
            possible_moves = [(row+1, col+1), (row+1, col-1)]
        
        
    
    return possible_moves


def drawPossibleMoves(selected):#draw said possible moves
    #This segment makes sure to clear the possible moves before
    _VARS['highlight'].fill((0,0,0,0))
    _VARS['surf'].blit(_VARS['highlight'])

    #we get the array of possible moves
    possible_moves=getPossibleMoves(selected)
    
    #check if its full
    if possible_moves:
        #loop over it
        for possible_move in possible_moves:
            col, row = possible_move
            #our trusty formula to go from matrice to grid
            x = _VARS['gridOrigin'][0] + (CELLDIMX*row)+_VARS['lineWidth']/2 + CELLDIMX/2
            y = _VARS['gridOrigin'][1] + (CELLDIMY*col)+_VARS['lineWidth']/2 + CELLDIMY/2
            center = (x,y)
            
            pygame.draw.circle(_VARS['highlight'], HIGHLIGHT, center=center, radius=CELLDIMX/3)
        
        _VARS['surf'].blit(_VARS['highlight'])


#main game loop
def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    _VARS['highlight'] = pygame.Surface(SCREENSIZE, pygame.SRCALPHA)
    running = True
    selected = False
    while running:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running = False
            #This checks for clicks
            if event.type ==pygame.MOUSEBUTTONUP:
                selected = selectedPieceCoordinates()
           
        _VARS['surf'].fill('grey')
        
        drawBoard()
        placePieces()
        if selected:
            drawHighlight(selected)
            drawPossibleMoves(selected)
        
        pygame.display.update()

if __name__ == '__main__':
    main()