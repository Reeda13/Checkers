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
        return int(row),int(col)

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
    _VARS['surf'].blit(_VARS['highlight'], (0,0))

    #the selected variable is a tuple storing the row and col of the cell we clicked in
    if selected:
        #extract the row and col
        row,col = selected
        #calculate the coordinates
        x = _VARS['gridOrigin'][0] + (CELLDIMX*col)+_VARS['lineWidth']/2
        y = _VARS['gridOrigin'][1] + (CELLDIMY*row)+_VARS['lineWidth']/2
        #draw the highlight
        pygame.draw.rect(_VARS['highlight'], HIGHLIGHT, (x,y,CELLDIMX,CELLDIMY))
        _VARS['surf'].blit(_VARS['highlight'], (0,0))

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
            
            #for kings    
            elif piecesmap[col][row] == 'W':
                drawPieces(center, CELLDIMX/2, 'orange')
                drawPieces(center, CELLDIMX/2.5, 'white')
            elif piecesmap[col][row] == 'B':
                drawPieces(center, CELLDIMX/2, 'yellow')
                drawPieces(center, CELLDIMX/2.5, 'black')

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

def sameColor(old, new): #helper function to check if 2 pieces are same color
    x,y = old
    dx, dy = new
    if piecesmap[x][y] and piecesmap[dx][dy]:
        return piecesmap[x][y].lower() == piecesmap[dx][dy].lower()

def oppositeColor(old,new): #helper function to check if 2 pieces are opposite color
    x,y = old
    dx, dy = new
    if 0<=dx<=7 and 0<=dy<=7:
        if piecesmap[x][y]  and piecesmap[dx][dy]:
            return piecesmap[x][y].lower() !=piecesmap[dx][dy].lower()

def makeKing(row,col):
    if piecesmap[row][col] == 'w':
        piecesmap[row][col] = 'W'
    elif piecesmap[row][col] == 'b':
        piecesmap[row][col] = 'B'

def isKing(row, col):
    if piecesmap[row][col] in ('W', 'B'):
        return True
    else:
        return False

#rework on the getpossiblemoves
def getPossibleMoves(selected):
        
    #initialize  possible moves
    possible_moves = []
    captured_pieces = []

    if selected:
        row,col = selected
        directions = []
        #check if king captured
        
            
            #by doing this we remove the need to repeat for the other color
        if piecesmap[row][col]=='w':
            directions = [(-1,1),(-1, -1)]

        elif piecesmap[row][col] == 'b':
            directions = [(1,1), (1,-1)]

        elif isKing(row, col):
            directions = [(1,1),(1,-1),(-1,-1),(-1,1)]

        if isKing(row,col):
            #to tackle kings mouvements we first loop all 4 diagonals        
            for dx,dy in directions:

                for i in range(1,8):
                    #if we encounter a piece of our own there is no point in continuing in that direction
                    if 0<=row+i*dx<=7 and 0<=col+i*dy<=7 and sameColor((row, col), (row+i*dx, col+i*dy)) :
                        break
                    #if we have 2 oppenents pieces diagonally adgacent to eachother
                    if 0<=row+i*dx<=7 and 0<=col+i*dy<=7 and oppositeColor((row, col), (row+i*dx, col+i*dy)) and 0<=row+i*dx+dx<=7 and 0<=col+i*dy+dy<=7 and not isEmpty(row+(i+1)*dx, col+(i+1)*dy) :
                        break
        
                    #loop in the direction
                    if 0<=row+i*dx<=7 and 0<=col+i*dy<=7 and isEmpty(row+i*dx, col+i*dy):    
                        possible_moves.append((row+i*dx, col+i*dy))




                    if oppositeColor((row,col),(row+i*dx, col+i*dy)) and 0<=row+i*dx+dx<=7 and 0<=col+i*dy+dy<=7 and isEmpty(row+i*dx+dx, col+i*dy+dy) :
                        for x,y in directions:
                            newrow,newcol = row+2*dx, col+2*dy
                            if 0<=newrow+x<=7 and 0<=newcol+y<=7 and oppositeColor((row,col),(newrow+x,newcol+y)) and 0<=newrow+2*x<=7 and 0<=newcol+2*y<=7 and isEmpty(newrow+2*x, newcol+2*y):
                                possible_moves.append((newrow+2*x, newcol+2*y))
                                captured_pieces.append((row+dx, col+dx))
                                captured_pieces.append((newrow+x,newcol+y))
                        
                        captured_pieces.append((row+i*dx, col+i*dy))
        else:
            #loop over the 2 new squares
            for dx,dy in directions:
                #making sure we are on bounds
                if 0<=row+dx<=7 and 0<=col+dy<=7 and isEmpty(row+dx, col+dy):
                    #The last 2 variables are supposed to be the captured piece coordinates
                    possible_moves.append((row+dx, col+dy))
                        
                    #checking for captures
                if oppositeColor((row,col),(row+dx,col+dy)) and 0<=row+2*dx<=7 and 0<=col+2*dy<=7 and isEmpty(row+2*dx, col+2*dy):
                    #double captures
                    for x,y in directions:
                        newrow,newcol = row+2*dx, col+2*dy
                        if 0<=newrow+x<=7 and 0<=newcol+y<=7 and oppositeColor((row,col),(newrow+x,newcol+y)) and 0<=newrow+2*x<=7 and 0<=newcol+2*y<=7 and isEmpty(newrow+2*x, newcol+2*y):
                            possible_moves.append((newrow+2*x, newcol+2*y))
                            captured_pieces.append((row+dx, col+dx))
                            captured_pieces.append((newrow+x,newcol+y))
            
                        #we append the new location of the piece and the captured piece row and col
                    possible_moves.append((row+2*dx, col+2*dy))
                    captured_pieces.append((row+dx, col+dy, row+2*dx, col+2*dy))
                        
        return possible_moves, captured_pieces



def drawPossibleMoves(selected):#draw said possible moves
    #This segment makes sure to clear the possible moves before
    _VARS['highlight'].fill((0,0,0,0))
    _VARS['surf'].blit(_VARS['highlight'], (0,0))

    rect = None

    #we get the array of possible moves
    possible_moves =getPossibleMoves(selected)[0]
    
    #check if its full
    if possible_moves:
        #loop over it
        for possible_move in possible_moves:
            #since getpossiblemoves returns 4 variables we extract 4 tho we use 2
            col, row = possible_move
            #our trusty formula to go from matrice to grid
            x = _VARS['gridOrigin'][0] + (CELLDIMX*row)+_VARS['lineWidth']/2 + CELLDIMX/2
            y = _VARS['gridOrigin'][1] + (CELLDIMY*col)+_VARS['lineWidth']/2 + CELLDIMY/2
            center = (x,y)
            #the possible moves
            pygame.draw.circle(_VARS['highlight'], HIGHLIGHT, center=center, radius=CELLDIMX/3)
            
            #the next segment is an aesthetic touch, a hover effect on those said possible move
            rect = pygame.Rect(x-CELLDIMX/2,y-CELLDIMY/2,CELLDIMX,CELLDIMY)
            pos = pygame.mouse.get_pos()
            ishovered = rect.collidepoint(pos)
            if ishovered:
                pygame.draw.rect(_VARS['highlight'],HIGHLIGHT, (x-CELLDIMX/2,y-CELLDIMY/2,CELLDIMX,CELLDIMY))
            
        _VARS['surf'].blit(_VARS['highlight'], (0,0))
    

def clickedPossibleMove(selected, pos):#This function checks if user clicked one of the possible moves squares
    rowcol = getRowCol(pos)
    if rowcol:
        #there is a weird glitch in the program that reverses them i cant figure it why but I can work around it
        col,row = rowcol 
        #convert them to int
        col, row = int(col), int(row)
        possible_moves, captured_pieces = getPossibleMoves(selected)
        #check if the clicked location is in possible moves        
        if possible_moves:
            #x = row, y=col, a=captured piece row, b=captured piece col
            for x,y in possible_moves:
                if row == x and col == y:
                    return (x,y), captured_pieces


def movement(selected, pos,turn):
    if selected :
        chosen_move = []
        captured_pieces=[]
        
        clicked = clickedPossibleMove(selected, pos)
        if clicked:
            if clicked[0]:
                chosen_move = clicked[0]
            else:
                chosen_move=[]

            if clicked[1]:
                captured_pieces = clicked[1]
            else:
                captured_pieces = [] 
        
        
        if chosen_move:
            
            row, col = selected
            #we extract the 4 variables form possible moves
            newrow, newcol = chosen_move
            if captured_pieces:
                for capturedpiece in captured_pieces:
                    if len(capturedpiece) == 4:
                        if newrow == capturedpiece[2] and newcol == capturedpiece[3]:
                            piecesmap[capturedpiece[0]][capturedpiece[1]] = ''

                    else:
                        capturedrow, capturedcol = capturedpiece
                        #remove the captured piece
                        piecesmap[capturedrow][capturedcol] =''
            #relocate the piece, the next line is to get the pieces color
            
            piecesmap[newrow][newcol] = piecesmap[row][col]
            #remove the original
            piecesmap[row][col] = ''
            if newrow == 0 or newrow ==7:
                makeKing(newrow, newcol)
            
            turn+=1
        return turn


#main game loop
def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    _VARS['highlight'] = pygame.Surface(SCREENSIZE, pygame.SRCALPHA)
    running = True
    selected = False
    #for turnbased
    turn = 0
    turns = {0: 'w', 1:'b'}

    while running:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running = False
            #This checks for clicks
            if event.type ==pygame.MOUSEBUTTONUP:

                if selected and piecesmap[selected[0]][selected[1]].lower() == turns[turn%2]: 
                    turn = movement(selected, pygame.mouse.get_pos(),turn)
                    
                selected = selectedPieceCoordinates()



        _VARS['surf'].fill('grey')
        
        drawBoard()
        placePieces()
        if selected and piecesmap[selected[0]][selected[1]].lower() == turns[turn%2]:
            drawHighlight(selected)
            drawPossibleMoves(selected)


        pygame.display.update()


if __name__ == '__main__':
    main()