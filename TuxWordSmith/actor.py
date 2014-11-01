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
import os,string,math,random,time,sys
from random import random

import pygame
from pygame.locals import *

DEBUG=False
global images

class Actor(pygame.sprite.Sprite):
	
	def load_once(self,fname,rotozoom,tilesize,images):
		
		if images.has_key(fname):
			rect=images[fname].get_rect()
			return images[fname].subsurface(rect)
		else:
			images[fname]=pygame.image.load(fname)
			if rotozoom:
				w=images[fname].get_rect()[2]
				h=images[fname].get_rect()[3]
				tilesize_x=tilesize
				tilesize_y=tilesize
				if w!=0:tilesize_y=int(tilesize*h/w)
				images[fname]=pygame.transform.scale(images[fname],(tilesize_x,tilesize_y))
				images[fname].set_colorkey((255,255,255))
			rect=images[fname].get_rect()
			return images[fname].subsurface(rect)

	
#	def __init__(self,indir,dt,w_scene,h_scene,xc,yc,z,smk):# "smk"==specific_maneuver_key
	def __init__(self,indir,gc,xc,yc,z,smk,rotozoom_tilesize,images):# "smk"==specific_maneuver_key
		
		pygame.sprite.Sprite.__init__(self)
		
		self.tlast=time.time()
		self.dt=gc['TSLEEP_ANIMATION']['value']
		self.w_scene=gc['WIN_W']['value']
		self.h_scene=gc['WIN_H']['value']
		self.rotozoom_tilesize=rotozoom_tilesize
		
		self.AmNone=False
		if indir[-4:]=='None':
			self.AmNone=True
			
		infile=os.path.join(indir,'config')
		inf=open(infile)
		self.config=eval(inf.read())
		inf.close()
		
		"""
			passing xc yc or z allows to overwrite None values in 
			config['maneuvers'] and redefine config['preferences'] xc,yc,z
		"""
		if xc:self.config['preferences']['xc']=xc
		if yc:self.config['preferences']['yc']=yc
		if z: self.config['preferences']['z'] =z
		for key in self.config['maneuvers'].keys():
			for sidx in range(len(self.config['maneuvers'][key])):
				if DEBUG:print self.config['maneuvers'][key]
				if self.config['maneuvers'][key][sidx][1]==None:self.config['maneuvers'][key][sidx][1]=self.config['preferences']['xc']
				if self.config['maneuvers'][key][sidx][2]==None:self.config['maneuvers'][key][sidx][2]=self.config['preferences']['yc']
				
		self.images={}
		self.sequences=self.config['sequences']
		self.maneuvers=self.config['maneuvers']
		
		self.xdest=None
		self.ydest=None
		self.maneuver=None
		self.pyld_idx=None
		self.sequence_idx=None
		self.surface=None
		self.xc=None
		self.yc=None
		self.stationary_idx=None
		self.maneuver_queue=[]

		#this before b/c might need rescale
		self.x=0
		self.y=0
		self.z=self.config['preferences']['z']
		if self.AmNone:return
		
		for key in self.config['sequences'].keys():
			for idx in range(len(self.config['sequences'][key])):
				
				imgfile=self.config['sequences'][key][idx]['img']
				surf=self.load_once(imgfile,self.rotozoom_tilesize,gc['TILESIZE']['value'],images)
				if self.z==999:surf=pygame.transform.scale(surf,(w_scene,h_scene))
				self.config['sequences'][key][idx]['img']=surf
		
		#these after b/c need surf		
		self.x=self.config['preferences']['xc']-surf.get_width()/2
		self.y=self.config['preferences']['yc']-surf.get_height()/2
		
		
		


	def queue(self,which):
		if self.AmNone:return
		
		#Allow multiple maneuvers to be queued and executed in order: (Nice feature, huh?)
		self.maneuver_queue.append(which)
	
	def begin_maneuver(self,which):
		if self.AmNone:return
		
		#random from maneuver groups, or specific
		maneuver_name=None
		if self.config['maneuver_groups'].has_key(which):
			if len(self.config['maneuver_groups'][which])==0:return
			idx=int(len(self.config['maneuver_groups'][which])*random())
			maneuver_name=self.config['maneuver_groups'][which][idx]
		elif self.config['maneuvers'].has_key(which):
			maneuver_name=self.config['maneuvers'][which]
		else:return
		
		if DEBUG:print maneuver_name
		
		#print "%s starting: %s"%(self.config['preferences']['name'],which)
		del self.maneuver
		self.maneuver=self.maneuvers[maneuver_name]
		self.pyld_idx=0
		self.sequence_idx=0
		
		del self.surface
		self.surface=self.sequences[self.maneuvers[maneuver_name][self.pyld_idx][0]][self.sequence_idx]['img']
		
		self.xc=self.x+self.surface.get_width()/2
		self.yc=self.y+self.surface.get_height()/2
		self.xdest=self.maneuver[self.pyld_idx][1]
		self.ydest=self.maneuver[self.pyld_idx][2]
		self.tlast=time.time()
		
		if self.xdest==-999:self.stationary_idx=0
		
		
		
	def render(self,t,scene,centerline,dx):
		if self.AmNone:return
		
		if not self.surface and not len(self.maneuver_queue):return
		if not self.xdest and len(self.maneuver_queue):
			next_maneuver_name=self.maneuver_queue.pop(0)
			self.begin_maneuver(next_maneuver_name)
		
		if not self.surface:return
			
		if t-self.tlast>self.dt:self.tlast=t
		else:
			if self.surface:scene.blit(self.surface,(self.x,self.y))
			return
		
		if not self.xdest or not self.ydest:
			scene.blit(self.surface,(self.x,self.y))
			return
		
		next_pyld_flag=0
		
		if self.xdest!=-999:
			dx=self.sequences[self.maneuver[self.pyld_idx][0]][self.sequence_idx]['dx']
			dy=self.sequences[self.maneuver[self.pyld_idx][0]][self.sequence_idx]['dy']
			self.x+=dx;self.xc+=dx
			self.y+=dy;self.yc+=dy
		
			scene.blit(self.surface,(self.x,self.y))
			
			self.sequence_idx+=1
			if self.sequence_idx>=len(self.sequences[self.maneuver[self.pyld_idx][0]]):self.sequence_idx=0
			
			del self.surface
			self.surface=self.sequences[self.maneuver[self.pyld_idx][0]][self.sequence_idx]['img']
			
			#reset sequence_idx as necessary until reach dest this pyld,
			r2=2*pow(dx,2)+2*pow(dy,2)
			dist=pow((self.xdest-self.xc),2)+pow((self.ydest-self.yc),2)
			#print dist,r2
		
			if dist<=r2:
				next_pyld_flag=1

			del r2
			del dist	

		else:
			dx=self.sequences[self.maneuver[self.pyld_idx][0]][self.sequence_idx]['dx']
			dy=self.sequences[self.maneuver[self.pyld_idx][0]][self.sequence_idx]['dy']
			self.x+=dx;self.xc+=dx
			self.y+=dy;self.yc+=dy

			scene.blit(self.surface,(self.x,self.y))
			
			self.sequence_idx+=1
			if self.sequence_idx>=len(self.sequences[self.maneuver[self.pyld_idx][0]]):self.sequence_idx=0
			
			del self.surface
			self.surface=self.sequences[self.maneuver[self.pyld_idx][0]][self.sequence_idx]['img']
			
			self.stationary_idx+=1
			if self.stationary_idx>=self.ydest:
				next_pyld_flag=1
		


		if next_pyld_flag:
			self.sequence_idx=0
			self.pyld_idx+=1
			
			
			if self.pyld_idx>=len(self.maneuver):
				#print 'DONE'
				self.xdest=None
				self.ydest=None
				self.dx=0
				self.dy=0
				
			else:
				del self.surface
				self.surface=self.sequences[self.maneuver[self.pyld_idx][0]][self.sequence_idx]['img']
				self.xdest=self.maneuver[self.pyld_idx][1]
				self.ydest=self.maneuver[self.pyld_idx][2]
				
				self.tlast=t
				if self.xdest==-999:self.stationary_idx=0
				else:self.stationary_idx=None
