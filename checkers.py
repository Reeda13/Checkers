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
RED = (153,0,0)
LIGHTERED = (240, 0, 0)
GREEN = (0, 100, 0)
LIGHTGREEN = (0,200, 0)

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
        pygame.draw.line(_VARS['surf'],'black', (cont_x, cont_y), (CONTAINER_SIZE+cont_x, cont_y), 20)
        #bottom
        pygame.draw.line(_VARS['surf'],'black',(cont_x, CONTAINER_SIZE+cont_y),(CONTAINER_SIZE+cont_x, CONTAINER_SIZE+cont_y) , 20)
        #left
        pygame.draw.line(_VARS['surf'],'black', (cont_x, cont_y), (cont_x,CONTAINER_SIZE+ cont_y),  20)
        #right
        pygame.draw.line(_VARS['surf'],'black', (CONTAINER_SIZE+cont_x, cont_y), (CONTAINER_SIZE+cont_x, CONTAINER_SIZE+cont_y),20)

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

def inBound(row, col):
    return 0<=row<=7 and 0<=col<=7


def multiCaptureKings(piece, direction, piece_color=None,
                 captured=None, land_to_capture=None):

    if captured is None:
        captured = []

    if land_to_capture is None:
        land_to_capture = {}

    row, col = piece
    # Get the king's color only on the first call
    if piece_color is None:
        piece_color = piecesmap[row][col].lower()

    for dx, dy in direction:

        for i in range(1, 8):

            current = (row + i * dx, col + i * dy)

            if not inBound(*current):
                break

            # Already captured pieces are treated as empty
            if current in captured:
                continue

            current_piece = piecesmap[current[0]][current[1]]

            # Empty square
            if current_piece == '':
                continue

            # Friendly piece blocks this direction
            if current_piece.lower() == piece_color.lower():
                break

            # Enemy found
            if current_piece.lower() != piece_color.lower():

                enemy = current

                # Square immediately after enemy
                landing = (row+(i+1)*dx, col+(i+1)*dy)

                if not inBound(*landing):
                    break

                # Landing square must be empty
                if not isEmpty(*landing):
                    break

                new_captured = captured + [enemy]

                # King can land on any empty square beyond enemy
                j = i + 1

                while inBound(row+j*dx, col+j*dy):

                    landing = (row+j*dx, col+j*dy)

                    if not isEmpty(*landing):
                        break

                    # Store the COMPLETE capture chain
                    land_to_capture[landing] = new_captured.copy()

                    # Search all 4 directions from new position
                    multiCaptureKings(
                        landing,
                        direction,
                        piece_color,
                        new_captured,
                        land_to_capture
                    )

                    j += 1

                break

    return land_to_capture

def multiCapture(piece, direction, piece_color=None, captured=None, land_to_capture=None):
    #initializing captured and landtocapture
    if captured is None:
        captured = []
    if land_to_capture is None:
        land_to_capture = {}
    
    #origin coordinates
    row, col = piece

    if piece_color is None:
        piece_color = piecesmap[row][col]

    for dx, dy in direction:
        enemy = (row+dx, col+dy)
        landing = (row+2*dx, col+2*dy)
        if not inBound(*enemy):
            continue
        if not inBound(*landing):
            continue
        if isEmpty(*enemy):
            continue
        if piecesmap[enemy[0]][enemy[1]].lower() == piece_color.lower():
            continue

        if not isEmpty(*landing):
            continue
        if enemy in captured:
            continue

        new_captured = captured+[enemy]
        land_to_capture[landing] = new_captured.copy()
    
        multiCapture(landing, direction, piece_color, new_captured, land_to_capture)
    return land_to_capture



#rework on the getpossiblemoves
def getPossibleMoves(selected):
        
    #initialize  possible moves
    possible_moves = {}


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
                    if inBound(row+i*dx, col+i*dy) and not isEmpty(row+i*dx, col+i*dy):
                        break
        
                    #loop in the direction
                    if inBound(row+i*dx, col+i*dy) and isEmpty(row+i*dx, col+i*dy):    
                            possible_moves[(row+i*dx, col+i*dy)] = []

                    
            possible_moves.update(multiCaptureKings((row,col), directions))
        
        else: #if not king

            #loop over the 2 new squares
            for dx,dy in directions:
                #making sure we are on bounds
                if inBound(row+dx, col+dy) and isEmpty(row+dx, col+dy):
                    #The last 2 variables are supposed to be the captured piece coordinates
                    possible_moves[(row+dx, col+dy)] = []
                        
                    #checking for captures
            possible_moves.update(multiCapture((row,col), directions))               

        return possible_moves

#to force captures
def forcedCaptures(selected):
    forced_capture = {}
    possible_moves = {}
    
    if not selected:
        return

    #we loop over the whole board
    for row in range(8):
        for col in range(8):
            if isEmpty(row, col) or oppositeColor(selected, (row,col)):
                continue
            #we get all the possible moves
            possible_moves[(row,col)]= getPossibleMoves((row,col))
    

            
          

    if possible_moves:
        #for each piece
        for piece in possible_moves:
            #if it has a destination
            if possible_moves[piece]:
                #we loop over the destinations
                for destination in possible_moves[piece]:
                    #if it has a capture
                    capture = possible_moves[piece][destination]
                    if capture:
                        if piece in forced_capture:
                            forced_capture[piece][destination]=capture
                        else:
                            forced_capture[piece] = {destination: capture}
        #if legal moves isnt empty it means we have a capture
        if forced_capture:
            #if the selected piece has a capture
            if selected in forced_capture:
                return forced_capture[selected]
            #if it doesnt return nothing
            else: 
                return {}
        #if no captures return possible moves    
        return possible_moves[selected]
 


def drawPossibleMoves(selected):#draw said possible moves
    #This segment makes sure to clear the possible moves before
    _VARS['highlight'].fill((0,0,0,0))
    _VARS['surf'].blit(_VARS['highlight'], (0,0))

    rect = None

    #we get the array of possible moves
    possible_moves =forcedCaptures(selected)
    
    #check if its full
    if possible_moves:
        #loop over it
        for possible_move in possible_moves:
            #since get ossiblemoves returns 4 variables we extract 4 tho we use 2
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
        possible_moves_dict = forcedCaptures(selected)
        if possible_moves_dict:
            possible_moves = list(possible_moves_dict.keys())
        #check if the clicked location is in possible moves        
            if possible_moves:
            #x = row, y=col, a=captured piece row, b=captured piece col
                for x,y in possible_moves:
                    if row == x and col == y:
                        return (x,y), possible_moves_dict.get((x,y))


def movement(selected, pos,turn):
    
    if selected:
        chosen_move = []
        captures = []
        
        clicked = clickedPossibleMove(selected, pos)
        if clicked:
            if clicked[0]:
                chosen_move = clicked[0]
            if clicked[1]:
                captures = clicked[1]
        
        if chosen_move:
            row, col = selected

            newrow, newcol = chosen_move
            if captures:
                for x,y in captures:
                    piecesmap[x][y]=''

            piecesmap[newrow][newcol] = piecesmap[row][col]

            piecesmap[row][col] = ''
            if newrow in (0,7):
                makeKing(newrow, newcol)
            turn+=1
        return turn

def checkForWins(): #function to check if any side captured all pieces
    if not hasMoves(turns[turn%2]):
        if turns[turn%2] == 'w':
            return 'Black'
        else: return 'White'    
    white, black = 0,0
    for row in range(8):
        for col in range(8):
            if piecesmap[row][col].lower() == 'w':
                white +=1
            if piecesmap[row][col].lower() == 'b':
                black +=1
    if black == 0:
        return 'White'
    elif white == 0:
        return 'Black'
    
def hasMoves(color):
    possible_moves = {}
    for row in range(8):
        for col in range(8):
            if piecesmap[row][col].lower() != color:
                continue
            possible_moves =getPossibleMoves((row,col))
            if possible_moves:
                return True
    return False

def endScreen():

        winning_side = checkForWins()
        if winning_side:
            #Title
            font = pygame.font.SysFont("Helvetica", 80, bold=True)
            font.set_underline(True)
            text = font.render(f"{winning_side} wins!", True, (0,0,0))
            font.set_underline(False)

            #Buttons text
            smallfont = pygame.font.SysFont("Corbel", 40, bold=True)
            quit = smallfont.render("Quit", True, "White")
            play_again = smallfont.render("Play again", True, "White")
                        
            #Coloring background and blitting title
            _VARS['surf'].fill((37,114,38))
            _VARS['surf'].blit(text, (80,40))
                
            #border
            pygame.draw.rect(_VARS['surf'], "black", (10,10, 580, 580), 10)
            #get mouse position
            mouse = pygame.mouse.get_pos()
                
            #hovering over quit
            if 350<=mouse[0]<=550 and 400<=mouse[1]<=470:
                pygame.draw.rect(_VARS['surf'], LIGHTERED, (350, 400, 200, 70))
            else:
                pygame.draw.rect(_VARS['surf'], RED, (350, 400, 200, 70))
            _VARS['surf'].blit(quit, (410, 415))
                
            #Hovering over play again        
            if 50<=mouse[0]<=270 and 400<=mouse[1]<=470:
                pygame.draw.rect(_VARS['surf'], LIGHTGREEN, (50, 400, 220, 70))
            else:
                pygame.draw.rect(_VARS['surf'], GREEN, (50, 400, 220, 70))
            _VARS['surf'].blit(play_again, (70, 415))

            return True
        else:
            return False
        
def gameLoop(selected, end=False):
    #Filling everything
    _VARS['surf'].fill((49, 120, 35))

    #title on top of board
    font = pygame.font.SysFont("Helvetica", 100, bold=True)
    checkers_text = font.render("Checkers", True,(121, 217, 124))
    _VARS['surf'].blit(checkers_text, (70,20))
    
    if not end:   
        drawBoard()
        placePieces()
        if selected and piecesmap[selected[0]][selected[1]].lower() == turns[turn%2]:
                drawHighlight(selected)
                drawPossibleMoves(selected)
        
    
def resetBoard():
    global piecesmap
    piecesmap = np.zeros((8,8), dtype=str)
    for row in range(piecesmap.shape[0]):
        for col in range(piecesmap.shape[1]):
            if row in (0,1,2) and row%2 !=col%2:
                piecesmap[row][col] = 'b'
            elif row in (5,6,7) and row%2 != col%2:
                piecesmap[row][col] = 'w'

def mainMenu(main_menu):
    if main_menu:
        _VARS['surf'].fill((37,114, 38))

        #Border
        pygame.draw.rect(_VARS['surf'], (121, 217, 124), (20, 20, 560, 560), 10)

        #Title
        title = pygame.font.SysFont("Helvetica", 100, bold=True)
        title.set_underline(True)
        checkers_text = title.render("Checkers", True, (121, 217, 124))
        _VARS['surf'].blit(checkers_text, (70, 100))


        #watermark
        wtermark = pygame.font.SysFont("Corbel", 20)
        maker = wtermark.render("Made by: Reeda13", True, "black") 
        _VARS['surf'].blit(maker, (400,550))


        #checkers in the middle
        pygame.draw.circle(_VARS['surf'], "black", (300,350), 100)
        pygame.draw.circle(_VARS['surf'], (42,42,42), (300,350), 90)
        pygame.draw.circle(_VARS['surf'], "black", (300,350), 80)
        pygame.draw.circle(_VARS['surf'], (42,42,42), (300,350), 70)
        pygame.draw.circle(_VARS['surf'], "black", (300,350), 60)
        pygame.draw.circle(_VARS['surf'], (42,42,42), (300,350), 50)
        pygame.draw.circle(_VARS['surf'], "black", (300,350), 40)
        pygame.draw.circle(_VARS['surf'], (42,42,42), (300,350), 30)
        pygame.draw.circle(_VARS['surf'], "black", (300,350), 20)
        pygame.draw.circle(_VARS['surf'], (42,42,42), (300,350), 10)


        #Buttons text
        smallfont = pygame.font.SysFont("Corbel", 40, bold=True)
        quit = smallfont.render("Quit", True, "White")
        play = smallfont.render("Play ", True, "White")
                        
                
        #get mouse position
        mouse = pygame.mouse.get_pos()
                
        #hovering over quit
        if 350<=mouse[0]<=550 and 460<=mouse[1]<=530:
            pygame.draw.rect(_VARS['surf'], LIGHTERED, (350, 460, 200, 70))
        else:
            pygame.draw.rect(_VARS['surf'], RED, (350, 460, 200, 70))
        _VARS['surf'].blit(quit, (410, 475))
                
            #Hovering over play        
        if 50<=mouse[0]<=270 and 460<=mouse[1]<=530:
            pygame.draw.rect(_VARS['surf'], LIGHTGREEN, (50, 460, 220, 70))
        else:
            pygame.draw.rect(_VARS['surf'], GREEN, (50, 460, 220, 70))
        _VARS['surf'].blit(play, (120, 475))

    else:
        return 
    
#main game loop
def main():
    pygame.init()
    pygame.font.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("Checkers")
    _VARS['highlight'] = pygame.Surface(SCREENSIZE, pygame.SRCALPHA)
    
    #Booleans for making track of the game
    running = True
    selected = False
    end = False
    main_menu = True
 

    #for turnbased
    global turn
    turn = 0
    global turns
    turns = {0: 'w', 1:'b'}

    while running:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running = False
            #This checks for clicks
            if event.type ==pygame.MOUSEBUTTONUP:

                if not(end) and selected and piecesmap[selected[0]][selected[1]].lower() == turns[turn%2]: 
                    turn = movement(selected, pygame.mouse.get_pos(),turn)
                selected = selectedPieceCoordinates()

                if end:
                    mouse = pygame.mouse.get_pos()
                    #quit 
                    if 350<=mouse[0]<=550 and 400<=mouse[1]<=470:
                        running = False
                    
                    #play again
                    if 50<=mouse[0]<=270 and 400<=mouse[1]<=470:
                        end = False
                        turn = 0
                        resetBoard()

                if main_menu:
                    mouse = pygame.mouse.get_pos()
                    #quit 
                    if 350<=mouse[0]<=550 and 460<=mouse[1]<=530:
                        running = False
                    
                    #play
                    if 50<=mouse[0]<=270 and 460<=mouse[1]<=530 and not end:
                        gameLoop(selected)
                        main_menu = False
                        
        if main_menu:
            mainMenu(main_menu)
        else: gameLoop(selected)
        
        end = endScreen()
        
        
        pygame.display.update()


if __name__ == '__main__':
    main()