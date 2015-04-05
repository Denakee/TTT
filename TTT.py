import sys, pygame
pygame.init()

#SIMPLE TIC TAC TOE GAME#
#Developed by Denakee	#
#Powered by pyGame	#

size = width, height = 600, 600 		#Define size of board
screen = pygame.display.set_mode(size)		#Define screen as the display we are using.
pygame.display.set_caption('Tic Tac Toe')	#Setting window title
playerTurn = 0				#Define which player starts (Don't make this a boolean as it can't be for games over 2 players)
white = 255, 255, 255			#Set some standard colors for later use (no alpha)	#
black = 0, 0, 0				#							#
red = 255, 0, 0				#							#
blue = 0, 255, 0			#							#
click = 0				#Define click to tell if the down key was pressed (boolean)
play = True				#Check if a game is finished or not
winBoxA = (0,0)
winBoxB = (0,0)

#Set up array for storing player piece locations
boardPiecePos = [[0]*3 for i in range(3)]

#		Image management		#

imageScale = (width /3 -4, height /3 -4) #<-called a tuple (cannot set individual values i.e. imageScale[0] = 1)
#call with imageScale[0] or [1]

#BoardClickField = [] #top left hand corner for each box
cornerPos = [range(4) for i in range(4)]
for i,j in [(a,b) for a in range(4) for b in range(4)]: #create table for top left hand image positions
	cornerPos[i][j] = ((width /3 *i),(height /3 *j))

#Load in icon images
#No alpha so must be on a white background
#^^Change at a later date^^
iconX = pygame.transform.scale(pygame.image.load("iconX.png"), imageScale)
iconO = pygame.transform.scale(pygame.image.load("iconO.png"), imageScale)

#						#

def drawBoard():		###Draws the lines for board###
	for i in range(1, 3):
		#Width generation first (x, y)
		pointA = width/30, height /3 *i
		pointB = width-width/30, height /3 *i
		pygame.draw.line(screen, black, pointA, pointB, 3)
		#Height generation
		pointA = width /3 *i, height/30 
		pointB = width /3 *i, height-height/30
		pygame.draw.line(screen, black, pointA, pointB, 3)
				###############################

				#####Switches player turns#####
def switchPlayer():
	global playerTurn
	
	if playerTurn == 1: playerTurn = 0
	else: playerTurn = 1
				###############################

				####Checks for moves (dito)####
def checkMove():
	global click
	global boardPiecePos
	global playerTurn
	global cornerPos
	if event.type == pygame.MOUSEBUTTONDOWN:
		click = 1	#Allow for check with button up	
	if event.type == pygame.MOUSEBUTTONUP and click == 1: #Check for mouse event press release
		#scan through locations to find which box the mouse clicked in
		mousePos = pygame.mouse.get_pos()
		for i,j in [(a,b) for a in range(3) for b in range(3)]: 
			#Check for mouse click location within the bounds of each box
			if (mousePos[0] > cornerPos[i][j][0] and
			mousePos[1] > cornerPos[i][j][1] and 
			mousePos[0] < cornerPos[i+1][j+1][0] and 
			mousePos[1] < cornerPos[i+1][j+1][1]):
				if boardPiecePos[i][j] != 1 and boardPiecePos[i][j] != 2:
					#Store move to position as playerTurn +1 as 0 is a blank location
					boardPiecePos[i][j] = playerTurn + 1
					#switch player turns
					switchPlayer()
					click = 0 #reset click
				###############################

def checkWin():			#####Determines the winner#####
	global playerTurn
	global play
	global winBoxA
	global winBoxB
	countEmpty = 0
	for i in range(3):
		for player in range(1,3):
			if ([a[i] for a in boardPiecePos] == [player]*3):  		#Checks y axis wins
				winBoxA = cornerPos[0][i]
				winBoxB = cornerPos[2][i]
				play = False
				
			elif (boardPiecePos[i] == [player]*3):				#Checks x axis wins
				winBoxA = cornerPos[i][0]
				winBoxB = cornerPos[i][2]
				play = False

			elif ([boardPiecePos[j][j] for j in range(3)] == [player]*3):	#Checks top left to bottom right
				winBoxA = cornerPos[0][0]
				winBoxB = cornerPos[2][2]
				play = False

			elif ([boardPiecePos[2-j][j] for j in range(3)] == [player]*3): #Checks top right to bottom left
				winBoxA = cornerPos[0][2]
				winBoxB = cornerPos[2][0]
				play = False
		for j in range(3):							#Checking for a tie game
			if (boardPiecePos[i][j] == 0):
				countEmpty += 1
	if countEmpty == 0:
		play = False
		winBoxA = cornerPos[1][1]
		winBoxB = cornerPos[1][1]
				###############################

def drawPieces():		####Draw in piece locations####
	global iconX
	global iconY
	for i,j in [(a,b) for a in range(3) for b in range(3)]:
		if boardPiecePos[i][j] == 1:
			#blit draws Surface (image) to a position	
			#blit(source, dest, area=None, special_flags = 0)
			screen.blit(iconX, tuple([x+2 for x in cornerPos[i][j]]))
		if boardPiecePos[i][j] == 2:
			#blit draws Surface (image) to a position	
			#blit(source, dest, area=None, special_flags = 0)
			screen.blit(iconO, tuple([x+2 for x in cornerPos[i][j]]))
				###############################

				######Draw in winning line#####
def drawWinLine():
	if play == False:
		pointA = winBoxA[0] + width/6, winBoxA[1] + height /6
		pointB = winBoxB[0] + width/6, winBoxB[1] + height /6
		pygame.draw.line(screen, red, pointA, pointB, 10)
				###############################

############################# START OF GAME SCRIPT ###################################
while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	screen.fill(white)		#Fill in background space with white
	drawBoard()			#Draw in board

	if play: #Check to see if game is finished
		checkMove()		#Check for player move
		checkWin()		#Check if a player won
	else:
		if event.type == pygame.MOUSEBUTTONDOWN:
			click = 1	#Allow for check with button up	
		if event.type == pygame.MOUSEBUTTONUP and click == 1: #Check for mouse event press release
			#Reset array for storing player piece locations
			boardPiecePos = [[0]*3 for i in range(3)]
			click = 0
			play = True	
	drawPieces()			#Draw in player Pieces
	drawWinLine()

	pygame.display.flip()
		
############################## END OF GAME SCRIPT #####################################
