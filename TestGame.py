# TestGame.py
#
# Copyright (C) 2016 Abhijit Patel Here
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General
# Public License as published by the Free Software
# Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General
# Public License along with this program; if not, write
# to the Free Software Foundation, Inc., 51 Franklin
# St, Fifth Floor, Boston, MA 02110-1301  USA
#Simulate
import random, sys, time, pygame
from pygame.locals import *
from gi.repository import Gtk
FPS= 30

FLASHSPEED = 500 #milliseconds
FLASHDELAY = 200 #milliseconds
BUTTONSIZE = 150
BUTTONGAP= 20
TIMEOUT = 4 #SECONDS

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (155,0,0)
BRIGHTRED= (255,0,0)
GREEN = (0,155,0)
BRIGHTGREEN= (0,255,0)
BLUE = (0,0,155)
BRIGHTBLUE= (0,0,255)
YELLOW = (155,155,0)
BRIGHTYELLOW=(255,255,0)
DARKGRAY =(40,40,40)
bgColor = BLACK


class simulate:
	def __init__(self):
		pass
	
	def run(self):
		#self.running = True		
		global FPSCLOCK, DISPLAYSURF, BASICFONT,  BASFONT, YELLOWRECT, BLUERECT, REDRECT, GREENRECT, XMARGIN, YMARGIN, WINDOWWIDTH, WINDOWHEIGHT, score

		
		screen = pygame.display.get_surface()
                WINDOWWIDTH = screen.get_width()
		WINDOWHEIGHT=screen.get_height() 
		FPSCLOCK= pygame.time.Clock()
		'''	WINDOWWIDTH = 1000
		WINDOWHEIGHT = 1000'''
		DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
		#DISPLAYSURF = screen
		XMARGIN = int ((WINDOWWIDTH - (2* BUTTONSIZE)-BUTTONGAP)/2)
		YMARGIN = int ((WINDOWHEIGHT - (2* BUTTONSIZE)-BUTTONGAP)/2)

		#rectObjects for every color
		YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
		BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN , BUTTONSIZE, BUTTONSIZE)
		REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAP , BUTTONSIZE, BUTTONSIZE)
		GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN + BUTTONSIZE + BUTTONGAP, BUTTONSIZE, BUTTONSIZE)	
		pygame.display.set_caption('SIMULATE')
		BASICFONT = pygame.font.Font('freesansbold.ttf', 16)	
		BASFONT = pygame.font.Font('freesansbold.ttf', 40)
		getStartMsg= BASFONT.render('WAIT FOR A SECOND....', True,BLACK)
		getStrRect= getStartMsg.get_rect()
		getStrRect.topleft= (10,80)
		DISPLAYSURF.fill(bgColor)
		DISPLAYSURF.blit(getStartMsg,getStrRect)
		pygame.display.update()
		pygame.time.wait(1000)
		
	
	
		#initial message to display	
		infoSurf = BASICFONT.render('Match the pattern by clicking on button or using the Q, W, A, S keys', True,DARKGRAY)
		infoRect = infoSurf.get_rect()
		infoRect.topleft = (10,10)
		#load sound files
		DISPLAYSURF.fill(bgColor)
		DISPLAYSURF.blit(infoSurf,infoRect)
		pygame.display.update()
		pygame.time.wait(500) 
		#sound files here
		'''try:
	            pygame.mixer.init()
       		except Exception, err:
          	  self.sound=False
            	print 'error with sound', err
		pygame.mixer.init()		
		if sound :
			BEEP1=pygame.mixer.Sound('/sounds/beep1.ogg')
			BEEP2=pygame.mixer.Sound('/sounds/beep2.ogg')
			BEEP3=pygame.mixer.Sound('/sounds/beep3.ogg')
			BEEP4=pygame.mixer.Sound('/sounds/beep4.ogg')
		
		'''
		#intialize
		pattern =[] # keeps the track of the pattern played!	
		currentStep = 0 #iterator for pattern list 
		lastClicktime = 0  #timestamp pf the player's last button press
		score = 0 # now this is obvious score of the player
		waitingForInput = False # bool Fasle when pattern is playing, True when player is clicking on buttons!
		#DISPLAYSURF.fill(WHITE)
		#bgColor=WHITE
		# main game loop
		while True:
			clickedButton = None
			DISPLAYSURF.fill(bgColor)
			drawButtons()
			
			scoreSurf = BASICFONT.render('pattern length: '+str(score),True, WHITE)
			scoreRect= scoreSurf.get_rect()
		
			scoreRect.topleft= (WINDOWWIDTH - 200, 10)
			DISPLAYSURF.blit(scoreSurf,scoreRect)
			
			DISPLAYSURF.blit(infoSurf, infoRect)
			pygame.display.update() #checkingg!!
			checkForQuit()
			# Pump GTK messages.
            		while Gtk.events_pending():
                		Gtk.main_iteration()
			#event handling loop
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONUP:
					mousex, mousey = event.pos
					clickedButton = getButtonClicked(mousex, mousey)
				elif event.type == KEYDOWN:
					if event.key == K_q:
						clickedButton = YELLOW
					elif event.key == K_w:
						clickedButton = BLUE
					elif event.key == K_a:
						clickedButton = RED
					elif event.key == K_s:
						clickedButton =GREEN
			if not waitingForInput: #play pattern
				pygame.display.update()
				pygame.time.wait(1000)
				pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
           			for button in pattern:
			                flashButtonAnnimation(button)
                			pygame.time.wait(FLASHDELAY)					
				
				waitingForInput=True
			else: #wait for player input
				if clickedButton and clickedButton == pattern[currentStep]:
					flashButtonAnnimation1(clickedButton)
					currentStep += 1
					lastClickTime = time.time()
				
					if currentStep== len(pattern):
						changeBackgroundAnnimation()
						score+=1
						#pattern=[]
						waitingForInput= False #resetting
						currentStep = 0 #resetting
				elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep!=0 and time.time() - lastClickTime > TIMEOUT): #pushed wrong button or time out!!!
					gameOverAnnimation()
					# reset all variables!					
					pattern = []
					currentStep = 0
					waitingForInput = False
					score= 0
					pygame.time.wait(1000)
					changeBackgroundAnnimation()
			pygame.display.update()
			FPSCLOCK.tick(FPS)
	
def terminate():
		pygame.quit()
		sys.exit()
	
def checkForQuit():
		for event in pygame.event.get(QUIT):
		     if event.type==QUIT:
			terminate()
		     if pygame.type== QUIT:
			terminate()
		for event in pygame.event.get(KEYUP):
			if event.key == K_ESCAPE :
				terminate()
			pygame.event.post(event) #put the other keyup objects back!
		
def flashButtonAnnimation1(color, animationSpeed = 50):
		if color == YELLOW:
			#sound = BEEP1
			flashColor= WHITE
			rectangle = YELLOWRECT
		elif color== RED :
			#sound = BEEP2
			flashColor = WHITE
			rectangle = REDRECT
		elif color == BLUE :
			#sound = BEEP3
			flashColor= WHITE
			rectangle = BLUERECT
		elif color == GREEN:
			#sound = BEEP4
			flashColor = WHITE
			rectangle = GREENRECT
		origSurf = DISPLAYSURF.copy()
		flashSurf= pygame.Surface((BUTTONSIZE,BUTTONSIZE))
		flashSurf = flashSurf.convert_alpha()
		r, g, b = flashColor
		#sound.play()
		for start, end, step in ((0,255,1),(255,0,-1)):
			for alpha in range (start, end, animationSpeed * step):
				checkForQuit()
				DISPLAYSURF.blit(origSurf,(0, 0))
				flashSurf.fill((r, g, b, alpha))
				DISPLAYSURF.blit(flashSurf, rectangle.topleft)
				pygame.display.update()
				FPSCLOCK.tick(FPS)
		DISPLAYSURF.blit(origSurf,(0, 0))	
	
def flashButtonAnnimation(color, animationSpeed = 50):
		if color == YELLOW:
			#sound = BEEP1
			flashColor= BRIGHTYELLOW
			rectangle = YELLOWRECT
		elif color== RED :
			#sound = BEEP2
			flashColor = BRIGHTRED
			rectangle = REDRECT
		elif color == BLUE :
			#sound = BEEP3
			flashColor= BRIGHTBLUE
			rectangle = BLUERECT
		elif color == GREEN:
			#sound = BEEP4
			flashColor = BRIGHTGREEN
			rectangle = GREENRECT
		origSurf = DISPLAYSURF.copy()
		flashSurf= pygame.Surface((BUTTONSIZE,BUTTONSIZE))
		flashSurf = flashSurf.convert_alpha()
		r, g, b = flashColor
		#sound.play()
		for start, end, step in ((0,255,1),(255,0,-1)):
			for alpha in range (start, end, animationSpeed * step):
				checkForQuit()
				DISPLAYSURF.blit(origSurf,(0, 0))
				flashSurf.fill((r, g, b, alpha))
				DISPLAYSURF.blit(flashSurf, rectangle.topleft)
				pygame.display.update()
				FPSCLOCK.tick(FPS)
		DISPLAYSURF.blit(origSurf,(0, 0))
def drawButtons() :
		pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
		pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
		pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
		pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)
	
def changeBackgroundAnnimation(animationSpeed = 40):
		global bgColor
		newBgColor = (0, 0, 0)
		newBgSurf= pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
		newBgSurf=newBgSurf.convert_alpha()
		r, g, b= newBgColor
		for alpha in range (0, 255, animationSpeed):
			checkForQuit()
			DISPLAYSURF.fill(bgColor)
			newBgSurf.fill((r, g, b,alpha))
			DISPLAYSURF.blit(newBgSurf,(0, 0))
			drawButtons() # redraw buttons
			pygame.display.update()
			FPSCLOCK.tick(FPS)
		bgColor= newBgColor
	
def gameOverAnnimation(color= WHITE, animationSpeed= 50):
		origSurf=DISPLAYSURF.copy()
		flashSurf = pygame.Surface(DISPLAYSURF.get_size())
		flashSurf = flashSurf.convert_alpha()
		#BEEP1.play()
		#BEEP2.play()
		#BEEP3.play()
		#BEEP4.play()
		r, g, b = color	
		DISPLAYSURF.fill(bgColor)
		endSurf=BASICFONT.render('GAME OVER!! Try Again Score'+str((score*(score+1))/2),True,WHITE)
		endRect= endSurf.get_rect()
		endRect.topleft= (20,80)
		DISPLAYSURF.blit(endSurf,endRect)
		pygame.display.update()
		pygame.time.wait(2000)
		for i in range(3):
			for start, end, step in ((0, 255, 1), (255, 0, -1)):
				for alpha in range(start, end,animationSpeed * step):
					checkForQuit()
					flashSurf.fill((r, g, b, alpha))
					DISPLAYSURF.blit(origSurf, (0, 0))
					DISPLAYSURF.blit(flashSurf, (0, 0))
					drawButtons()
					pygame.display.update()
					FPSCLOCK.tick(FPS)
		
	
def getButtonClicked(x, y):
		if YELLOWRECT.collidepoint((x, y)):
			return YELLOW
		elif REDRECT.collidepoint((x, y)):
			return RED
		elif BLUERECT.collidepoint((x, y)):
			return BLUE
		elif GREENRECT.collidepoint((x, y)):
			return GREEN
def main():
	pygame.init()
	game=simulate()
	game.run()
	
if __name__ == '__main__':
		main()
	

