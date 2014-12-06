"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Support         :www.asymptopia.org/forum

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2015 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""

import pygame,os
from pygame.locals import *

class RoundButton(pygame.sprite.Sprite):
	
	def __init__(self,gc,msg,bfont):
		pygame.sprite.Sprite.__init__(self)
		
		#bfont:
		msg_surface=bfont.render(msg,1,gc['COLOR_FG_PLAYER1_TILE']['value'],gc['COLOR_BG_PLAYER1_TILE']['value'])
		
		#self.width=gc['GAME_BUTTON_W']['value']
		#self.height=gc['GAME_BUTTON_H']['value']
		self.width=msg_surface.get_width()*1.75
		self.height=self.width
		
		
		self.image = pygame.Surface((self.width,self.width))
		self.image.fill(gc['COLOR_BG']['value'])
		
		pygame.draw.circle(self.image,(0,0,0),self.image.get_rect().center,int(self.width/2),2)
		pygame.draw.circle(self.image,(255,255,255),self.image.get_rect().center,int(self.width/2-2),2)
		pygame.draw.circle(self.image,(0,0,0),self.image.get_rect().center,int(self.width/2-4),2)
		pygame.draw.ellipse(self.image,gc['COLOR_BG_PLAYER1_TILE']['value'],self.image.get_rect().inflate(-12,-12),0)
		
		#bfont:
		tlcx=self.width/2-msg_surface.get_width()/2
		tlcy=self.width/2-msg_surface.get_height()/2
		self.image.blit(msg_surface,(tlcx,tlcy))
		self.image.set_colorkey(gc['COLOR_BG']['value'])
		
		self.rect=self.image.get_rect()
		
		
	def get_height(self):
		return self.height
	
	def get_width(self):
		return self.width
