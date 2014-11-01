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
from spot import Spot


class Board(pygame.sprite.Group):
	
	def __init__(self,M,N,XC,YC,background_image,default_spot_image):
		pygame.sprite.Group.__init__(self)
		self.M=M
		self.N=N
		self.XC=XC
		self.YC=YC
		
		self.YTOP=None
		self.YBOT=None
		self.XLHS=None
		self.XRHS=None
		
		self.default_spot_image=default_spot_image
		self.map=None
		self.num_commited=0
		
		if background_image and not default_spot_image:self.make_background_spots(background_image)
		else:self.make_default_spots(default_spot_image)
		
		self.representation2D=[]
		for midx in range(self.M):
			self.representation2D.append([])
			for nidx in range(self.N):
				self.representation2D[midx].append(None)
				for spot in self.sprites():
					if spot.getMN()[0]==midx and spot.getMN()[1]==nidx:
						self.representation2D[midx][nidx]=spot
						
		
	
	def get_word_map(self):
		wm=[]
		for midx in range(self.M):
			wm.append([])
			for nidx in range(self.N):
				spot=self.representation2D[midx][nidx]
				if spot.guest:
					str_val=spot.guest.str_val
					uchar=spot.guest.uchar
					wm[midx].append(uchar)
					#counts[str_val]['count']+=1
					#counts[str_val]['mn'].append((midx,nidx))
				else:wm[midx].append(u'-')
		
		return wm
		
	def get_idx_map(self,letters):
		wm=[]
		for midx in range(self.M):
			wm.append([])
			for nidx in range(self.N):
				spot=self.representation2D[midx][nidx]
				if spot.guest:
					str_val=spot.guest.str_val
					uchar=spot.guest.uchar
					wm[midx].append("%2d"%letters.index(uchar))
					#counts[str_val]['count']+=1
					#counts[str_val]['mn'].append((midx,nidx))
				else:wm[midx].append('--')
		
		
		return wm
	
	def print_idx_map(self,letters):
		idx_map=self.get_idx_map(letters)
		for ridx in range(len(idx_map)):
			for cidx in range(len(idx_map[0])):
				print idx_map[ridx][cidx],
			print ''
	
	def print_word_map(self,letters):#letters not used; passed for likeness to print_idx_map()
		word_map=self.get_word_map()
		for ridx in range(len(word_map)):
			for cidx in range(len(word_map[0])):
				print word_map[ridx][cidx].encode('latin1'),
			print ''
			
	def get_map(self):#return meta info as well...
		
		counts={}
		counts['+']={'count':0,'mn':[]}
		counts['-']={'count':0,'mn':[]}
		counts['*']={'count':0,'mn':[]}
		counts['/']={'count':0,'mn':[]}
		counts['=']={'count':0,'mn':[]}
		for idx in range(21):counts[`float(idx)`]={'count':0,'mn':[]}
		
		m=[]
		for midx in range(self.M):
			m.append([])
			for nidx in range(self.N):
				spot=self.representation2D[midx][nidx]
				if spot.guest:
					str_val=spot.guest.str_val
					m[midx].append(str_val)
					counts[str_val]['count']+=1
					counts[str_val]['mn'].append((midx,nidx))
				else:m[midx].append('')
		
		return(m,counts)
	
			
	def check4guest(self,m,n):
		if m<0 or m>self.M-1 or n<0 or n>self.N-1:return(0)
		spot=self.get_spotMN(m,n)
		if spot.guest==None:return(0)
		else:return(1)
		
	def get_listofheads(self):
		heads=[]
		for spot in self.sprites():
			if spot.guest:
				if spot.AMHEAD:heads.append(spot)
		return(heads)			
	
	def clear_spots(self):
		for spot in self.sprites():
			spot.remove(self)
	
	def get_spotMN(self,m,n):
		for spot in self.sprites():
			MN=spot.getMN()
			if MN[0]==m and MN[1]==n:
				return(spot)
	
	def take_guestMN(self,tile,m,n):
		for spot in self.sprites():
			MN=spot.getMN()
			if MN[0]==m and MN[1]==n:
				spot.take_guest(tile,1)
				return(spot)
	
	def get_num_commited(self):
		return(self.num_commited)
	
	def increment_num_commited(self):
		self.num_commited=self.num_commited+1
	
	def get_guest_by_str(self,str_val):
		for spot in self.sprites():
			if spot.guest and spot.guest.str_val==str_val:
				return spot.pop_guest()
		return(None)
			
	def get_spots(self):
		return(self.sprites())
	
	#SPOT MAKERS:
	def make_background_spots(self,background_image):
		for midx in range(self.M):
			for nidx in range(self.N):
				#print 'need to break-up background image!'
				self.add(Spot(default_spot_image,midx,nidx))#change to background_tile
	
	def make_default_spots(self,default_spot_image):
		XC=self.XC
		YC=self.YC
		M=self.M
		N=self.N
		
		self.YTOP=YC-int((M/2.)*default_spot_image.get_height())
		self.YBOT=YC+int((M/2.)*default_spot_image.get_height())
		self.XLHS=XC-int((N/2.)*default_spot_image.get_width())
		self.XRHS=XC+int((N/2.)*default_spot_image.get_width())
		
		for midx in range(0,M):
			for nidx in range(0,N):
				spot=Spot(default_spot_image,midx,nidx,'REG')
				w=spot.image.get_width()
				h=spot.image.get_height()
				spot.rect.center=(	XC+int((-N/2.+nidx+.5)*w),YC+int(	(-M/2.+midx+.5)*h)	)
				self.add(spot)
							
	
