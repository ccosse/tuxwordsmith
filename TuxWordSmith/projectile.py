#!/usr/bin/python
"""
/***************************************************************************

	Author			:Charles B. Cosse 
	
	Email			:ccosse@gmail.com
					
	Website			:www.asymptopia.org
	
	Copyright		:(C) 2002-2007 Asymptopia Software.
	
 ***************************************************************************/
"""

from math import *
import sys,os,time,copy
from os.path import join
from random import random
import pygame
from pygame.locals import *
from packages import *

class Projectile(pygame.sprite.Sprite):
	def __init__(self,pkg):
		#print len(pkg)
		#print pkg
		
		#tblow,radius,x0,y0,vx0,vy0,ay,r,g,b,tl
		#tblow,dtblow,radius,x0,dx0,y0,dy0,vx0,dvx0,vy0,dvy0,ay,r,dr,g,dg,b,db,tl,dtl
		#   0     1      2    3   4  5  6    7   8    9   10  11 1213 1415 1617  1819
		pygame.sprite.Sprite.__init__(self)
		self.pkg=pkg
		self.tblow=pkg[0]
		self.dtblow=pkg[1]
		self.radius=pkg[2]
		self.x=pkg[3]
		self.y=pkg[5]
		self.x0=pkg[3]
		self.y0=pkg[5]
		self.vx=pkg[7]
		self.vy=pkg[9]
		self.vx0=pkg[7]
		self.vy0=pkg[9]
		self.ay=pkg[11]
		self.r=pkg[12]
		self.g=pkg[14]
		self.b=pkg[16]
		self.tail_length=pkg[19]
		self.tail=[]
		self.pyld=None
		self.image=pygame.Surface((int(self.radius),int(self.radius)))
		self.image.fill((self.r,self.g,self.b))
		self.rect=pygame.Rect(self.x0,self.y0,self.radius,self.radius)
		
	def killall(self):
		for sp in self.pyld.sprites():
			sp.killall()
			sp.kill()
		
	def update(self,fw_scaleFactor,t,dt,group):
		if t<self.tblow:return
		tel=t-self.tblow
		if tel>self.pkg[18]:self.kill()
		
		c=self.image.get_at(self.image.get_rect().center)
		self.image.fill((c[0]*fw_scaleFactor,c[1]*fw_scaleFactor,c[2]*fw_scaleFactor))
		self.r=c[0]
		self.g=c[1]
		self.b=c[2]
		self.vx=self.vx0#+self.ax*tel
		self.vy=float(self.vy0)+float(self.ay)*float(tel)
		
		dx=self.vx*float(dt)
		dy=self.vy*float(dt)
		self.x+=dx
		self.y+=dy
		self.rect.center=(self.x,self.y)
		
		self.tail.insert(0,self.rect.center)
		if len(self.tail)>self.tail_length:self.tail.pop()
		
		for sp in self.pyld.sprites():
			if t>sp.tblow:
				sp.x=self.x
				sp.y=self.y
				sp.rect=pygame.Rect(self.rect[0],self.rect[1],sp.rect[2],sp.rect[3])
				sp.vx0=self.vx+sp.vx0
				sp.vy0=self.vy+sp.vy0
				sp.add(group)
				sp.remove(self.pyld)
				
		

def get_rand(x,dx):
	rval=float(x)+float(dx)*(1.-2.*random())
	return rval

class FWOverlay:
	def __init__(self,screen,dt,fw_dt_launch,fw_scaleFactor):
		self.screen=screen
		self.w=self.screen.get_size()[0]
		self.h=self.screen.get_size()[1]
		self.fw_scaleFactor=fw_scaleFactor
		self.pi=acos(-1.)
		self.fw_dt_launch=fw_dt_launch
		self.t=time.time()
		self.tlast=self.t
		self.tlastlaunch=self.t
		self.dt=dt
		self.projectiles=projectiles=pygame.sprite.RenderClear()
		self.pkgs=mkpkgs(self.w,self.h)
		self.ntypes=len(self.pkgs)
		
	
	def reset(self):
		self.projectiles=projectiles=pygame.sprite.RenderClear()
			
	def make_volley(self,N):
		
		for idx in range(int(N)):
			ftype=int(floor(self.ntypes*random()))
			#ftype=0
			pkg=self.getpkg(ftype)
			#if idx==(N-1):
			#	pkg=self.getpkg(self.ntypes-1)
			pkgname=pkg.keys()[0]
			
			
			self.tlast=self.t
			self.t=time.time()
			p=self.build(self.t+idx*self.fw_dt_launch,pkg[pkgname])
			self.projectiles.add(p)
			#print pkgname
		
	def getn(self,t0,n,pkgi):
		pi=self.pi
		group=pygame.sprite.RenderClear()
		
	   	CL=pkgi[24]														#colorlock
		r=g=b=0
		if CL:
			r=get_rand(pkgi[12],pkgi[13])
			g=get_rand(pkgi[14],pkgi[15])
			b=get_rand(pkgi[16],pkgi[17])
			
		for idx in range(int(n)):
		
			#tblow,dtblow,r,x0,dx0,y0,dy0,vx0,dvx0,vy0,dvy0,ay, r,dr, g,dg, b, db,ttl, tl, n, dn, ringflag tail colorlock
			#  0     1    2 3  4   5   6   7   8   9    10  11 12 13  14 15 16 17  18  19   20 21     22     23     24
			pkg=[]
			
			#theta=random()*2.*pi
			
			pkg.append(t0+get_rand(pkgi[0],pkgi[1]))					#0
			pkg.append(random()*pkgi[1])								#1
			pkg.append(pkgi[2])#radius									#2
			pkg.append(get_rand(pkgi[3],pkgi[4]))						#3
			pkg.append(None)											#4
			pkg.append(get_rand(pkgi[5],pkgi[6]))						#5
			pkg.append(None)											#6
			
			
			if pkgi[22]:
				v=pkgi[7]
				theta=get_rand(pkgi[9],pkgi[10])
				pkg.append(v*cos(theta))
				pkg.append(None)
				pkg.append(v*sin(theta))
				pkg.append(None)
				
			else:
				v=get_rand(pkgi[7],pkgi[8])
				theta=get_rand(pkgi[9],pkgi[10])
				pkg.append(v*cos(theta))
				pkg.append(None)
				pkg.append(v*sin(theta))
				pkg.append(None)
			
			
			pkg.append(pkgi[11])#ay
			if CL:
				pkg.append(r)
				pkg.append(None)
				pkg.append(g)
				pkg.append(None)
				pkg.append(b)
				pkg.append(None)
			else:
				pkg.append(get_rand(pkgi[12],pkgi[13]))
				pkg.append(None)
				pkg.append(get_rand(pkgi[14],pkgi[15]))
				pkg.append(None)
				pkg.append(get_rand(pkgi[16],pkgi[17]))
				pkg.append(None)
			
			pkg.append(pkgi[18])						#18
			pkg.append(pkgi[19])						#19
			
			pkg.append(None)							#20
			pkg.append(None)							#21
			pkg.append(None)							#22
			pkg.append(pkgi[23])						#23
			pkg.append(pkgi[24])						#24
			
			p=Projectile(pkg)
			p.pyld=pygame.sprite.RenderClear()
			group.add(p)
			
			
		return group
		
	def build(self,t0,pkg):
		#print 'building...'
		w=self.w
		h=self.h
		fw_scaleFactor=self.fw_scaleFactor
		n=get_rand(pkg[0][20],pkg[0][21])
		sp0=self.getn(t0,n,pkg[0]).sprites()[0]
		
		if len(pkg)>1:
			n=get_rand(pkg[1][20],pkg[1][21])
			sp0.pyld=self.getn(t0,n,pkg[1])
			if len(pkg)>2:
				for sp1 in sp0.pyld.sprites():
					n=get_rand(pkg[2][20],pkg[2][21])
					sp1.pyld=self.getn(t0,n,pkg[2])
				#problem: if 0, dont want to be children of zeroeth
				#	for sp in sp1.pyld.sprites():
				#		if sp.dtblow==0:sp.tblow=sp1.tblow#sets to parent time for boom-boom
				#"""		
					if len(pkg)>3:
						for sp2 in sp1.pyld.sprites():
							n=get_rand(pkg[3][20],pkg[3][21])
							sp2.pyld=self.getn(t0,n,pkg[3])
							for sp in sp2.pyld.sprites():
								if sp.dtblow==0:sp.tblow=sp2.tblow#sets to parent time for boom-boom
				#"""
		return sp0
	
	def getpkg(self,arg):
		if type(arg)==int:
			return self.pkgs[arg]
		else:
			for pkg in self.pkgs:
				if pkg.keys()[0]==arg:return pkg
			
			
		
	def tick(self):
		
		w=self.w
		h=self.h
		
		#print self.t,self.fw_dt_launch,fmod(self.t,self.fw_dt_launch)
		
		t=time.time()
		if t-self.tlast>=self.dt or self.t==self.tlast:
			#print t-self.tlast
			self.tlast=self.t
			self.t=t
			self.projectiles.update(self.fw_scaleFactor,self.t,self.t-self.tlast,self.projectiles)

		self.projectiles.draw(self.screen)
		
		for sp in self.projectiles.sprites():
			#color=sp.image.get_at((0,0))
			#if (color[0]+color[1]+color[2])<30:sp.killall();sp.kill()#this should be a param in config (color cutoff for sprite removal)
			if sp.rect[0]<0:sp.killall();sp.kill()
			elif sp.rect[0]>w or sp.rect[1]>h:sp.killall();sp.kill()
			
			#print len(sp.pkg)
			if not sp.pkg[23]:continue
			if len(sp.tail)<1:continue
			for tidx in range(len(sp.tail)-1):
				x0=sp.tail[tidx][0];
				y0=sp.tail[tidx][1];
				x1=sp.tail[tidx+1][0];
				y1=sp.tail[tidx+1][1];
				pygame.draw.line(self.screen,(sp.r/(tidx+1),sp.g/(tidx+1),sp.b/(tidx+1)),(x0,y0),(x1,y1))



if __name__=='__main__':
		
		screen = pygame.display.set_mode((1124,700),pygame.DOUBLEBUF)
		pygame.mouse.set_visible(1)
		fw_dt=.05
		fw_dt_launch=0.6
		fw_scaleFactor=.97
		
		fwoverlay=FWOverlay(screen,fw_dt,fw_dt_launch,fw_scaleFactor)
		
		RUNNING=True
		while RUNNING:
			screen.fill((0,0,0))
			fwoverlay.tick()
			pygame.display.flip()
			for event in pygame.event.get(KEYDOWN):
				if event.key==K_F4:pygame.display.toggle_fullscreen()
				else:RUNNING=False
			
			if len(fwoverlay.projectiles)==0:
				fwoverlay.make_volley(20)
