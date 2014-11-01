"""
/***************************************************************************

	Author			:Charles B. Cosse 
	
	Email			:ccosse@gmail.com
					
	Website			:www.asymptopia.org
	
	Copyright		:(C) 2002-2007 Asymptopia Software.
	
 ***************************************************************************/
"""

import pygame
from pygame.locals import *

class Spot(pygame.sprite.Sprite):
	def __init__(self,default_image,M,N,TYPE):
		
		"""
		previously default_image was fname; now it's surface, like Tile.
		"""
		
		pygame.sprite.Sprite.__init__(self)
		if default_image:
			#self.default_image= pygame.image.load(default_surface)
			self.default_image=default_image
			self.rect=self.default_image.get_rect()
			self.image=self.default_image
		else:
			self.default_image=None
			self.rect=pygame.Rect(0,0,0,0)
			self.image=None
		
		self.msg=""	
		self.guest=None
		self.locked=0
		self.M=M
		self.N=N
		self.TYPE=TYPE
		
		self.AMHEAD=0
		self.AMROWEXPR=0
		self.AMCOLEXPR=0
		self.ROWEXPRLENGTH=0
		self.COLEXPRLENGTH=0

	
	def setMN(self,M,N):
		self.M=M
		self.N=N
	
	def getMN(self):
		return((self.M,self.N))
		
	def take_guest(self,guest,use_guest_image):
		self.guest=guest
		#print 'guest=',guest
		self.guest.rect.center=self.rect.center
		if use_guest_image:self.image=guest.image

	def lock(self):
		self.locked=1
	
	def islocked(self):
		return(self.locked)

	def occupied(self):
		if self.guest==None:return(0)
		return(1)
		
	def pop_guest(self):
		self.image=self.default_image
		guest=self.guest
		self.guest=None
		return(guest)
		
	def update(self):
		pass
		
	
