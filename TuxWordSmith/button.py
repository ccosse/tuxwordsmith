"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2008 Asymptopia Software

    License         :GPL2

***********************************************************/
"""

import pygame,os
from pygame.locals import *

class Button(pygame.sprite.Sprite):
	
	def __init__(self,gc,msg,bfont):
		pygame.sprite.Sprite.__init__(self)
		
		self.width=gc['GAME_BUTTON_W']['value']
		self.height=gc['GAME_BUTTON_H']['value']
		
		self.image = pygame.Surface((self.width,self.height))
		self.image.fill(gc['COLOR_FG_PLAYER1_TILE']['value'])
		
		inner = pygame.Surface((self.width-2,self.height-2))
		inner.fill(gc['COLOR_BG_PLAYER1_TILE']['value'])
		self.image.blit(inner,(1,1))
		
		inner2 = pygame.Surface((self.width-4,self.height-4))
		inner2.fill(gc['COLOR_FG_PLAYER1_TILE']['value'])
		self.image.blit(inner2,(2,2))

		#bfont:
		msg_surface=bfont.render(msg,1,gc['COLOR_BG_PLAYER1_TILE']['value'],gc['COLOR_FG_PLAYER1_TILE']['value'])
		tlcx=self.width/2-msg_surface.get_width()/2
		tlcy=self.height/2-msg_surface.get_height()/2
		self.image.blit(msg_surface,(tlcx,tlcy))
		
		self.rect=self.image.get_rect()
		
		
	def get_height(self):
		return self.height
	
	def get_width(self):
		return self.width
