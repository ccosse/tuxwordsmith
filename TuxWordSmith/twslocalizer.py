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
from random import random

class TWS_Localizer:
	"""TWS_Localizer has game model.
	"""
	def __init__(self,board,game):
		self.board=board
		self.game=game#only used to update score
		self.board_map=None
		self.counts=None
		self.M=self.board.M
		self.N=self.board.N

	def update_board_map(self):
		#returns a 2D array of str_vals
		self.board_map,self.counts=self.board.get_map()
	
	def localize(self,submission):
		
		#check if proposed wc values on board:
		wc_list=[]
		for idx in range(len(submission)):
			if submission[idx][:3]=='WC:':
				val=submission[idx][3:]
				try:val=`float(val)`
				except:pass
				if self.counts[val]['count']==0:
					del wc_list
					return None
				val=submission[idx][3:]
				wc_list.append((val,idx))
		
		
		#check if board can satisfy wc_values' distance and neighbor requirements: (and under what conditions, i.e. row/col?) 
		ok_row=0
		ok_col=0
		if self.game.board.num_commited==0:
			ok_row=1
			ok_col=1
		if len(wc_list)<2:
			ok_row=1
			ok_col=1	
		for idx in range(len(wc_list)-1):
		#  try:
			dist=wc_list[idx+1][1]-wc_list[idx][1]
			#does this pair exist on board with this dist separation?
			for idx0 in range(len(self.counts[wc_list[idx][0]]['mn'])):
				for idx1 in range(len(self.counts[wc_list[idx+1][0]]['mn'])):
					dm=self.counts[wc_list[idx+1][0]]['mn'][idx1][0]-self.counts[wc_list[idx][0]]['mn'][idx0][0]
					dn=self.counts[wc_list[idx+1][0]]['mn'][idx1][1]-self.counts[wc_list[idx][0]]['mn'][idx0][1]
					if dm==dist:ok_col=1
					if dn==dist:ok_row=1
		#  except:print self.counts[`float(wc_list[idx][0])`]
		if ok_row or ok_col:pass
		else:return None
		
		#flip coin to decide whether to try row or col first:
		rand=int(random()*2)
		if rand==0:
			rlist=self.try_row(submission)
			if rlist:return(rlist)
			rlist=self.try_col(submission)
			if rlist:return(rlist)
		else:	
			rlist=self.try_col(submission)
			if rlist:return(rlist)
			rlist=self.try_row(submission)
			if rlist:return(rlist)
		return(None)
		
	def try_row(self,submission):	
		#print 'try_row'
		board_map=self.board_map
		M=self.M
		N=self.N
		if len(submission)==0:return(None)
		
		slim=len(submission)
		nlim=N-len(submission)+1
		
		MMIN=0
		if self.board.num_commited==0:MMIN=M/2
		
		NMIN=0
		if self.board.num_commited==0:NMIN=N/2-len(submission)/2
		if NMIN<0:NMIN=0
		
		for m in range(MMIN,M):
			for n in range(NMIN,nlim):
				ok=1
				for sidx in range(slim):
					if submission[sidx][:3]=='WC:':
						if board_map[m][n+sidx]==submission[sidx][3:]:
							dummy=0
							#print submission,'we have match:',submission[sidx],' at m,n = ',m,n+sidx
						else:ok=0
					elif board_map[m][n+sidx]=='':dummy=0
					else:
						#print 'ROW: setting->0 b/c board ',m,n+sidx,' !=\'\' ',board_map[m][n+sidx],submission[sidx][:3]
						ok=0;
				if ok==1:#head @(m,n)
					rlist=[]
					for idx in range(slim):
						tripple=[submission[idx],m,n+idx]
						#if tripple[0][:3]=='WC:':dummy=0  <-remove these after check;keep "WC:" in the value
						#else:rlist.append(tripple)
						rlist.append(tripple)
					
					rval=self.check_neighborhood(rlist)
					#print 'check_neighborhood returned:',rval
					
					#now remove "WC:"s
					for idx in range(slim-1,-1,-1):
						if rlist[idx][0][:3]=='WC:':x=rlist.pop(idx);del x
					
					if rval==1:return(rlist)
				
		return(None)
		
	def try_col(self,submission):	
		#print 'try_col'
		board_map=self.board_map
		M=self.M
		N=self.N
		if len(submission)==0:return(None)
		
		slim=len(submission)
		mlim=M-len(submission)+1

		MMIN=0
		if self.board.num_commited==0:MMIN=M/2-len(submission)/2
		if MMIN<0:MMIN=0
		
		NMIN=0
		if self.board.num_commited==0:NMIN=N/2

		for n in range(NMIN,N):
			for m in range(MMIN,mlim):
				ok=1
				for sidx in range(slim):
					if submission[sidx][:3]=='WC:':
						if board_map[m+sidx][n]==submission[sidx][3:]:
							#print submission,'we have match:',submission[sidx],' at m,n = ',m+sidx,n
							dummy=0
						else:ok=0
					elif board_map[m+sidx][n]=='':dummy=0
					else:
						#print 'COL: setting->0 b/c board ',m+sidx,n,' !=\'\' ',board_map[m+sidx][n],submission[sidx][:3]
						ok=0;
				
				if ok==1:#head @(m,n)
					rlist=[]
					for idx in range(slim):
						tripple=[submission[idx],m+idx,n]
						#if tripple[0][:3]=='WC:':dummy=0
						#else:rlist.append(tripple)
						rlist.append(tripple)

					rval=self.check_neighborhood(rlist)
					#print 'check_neighborhood returned:',rval
					
					#now remove "WC:"s
					for idx in range(slim-1,-1,-1):
						if rlist[idx][0][:3]=='WC:':x=rlist.pop(idx);del x
					
					if rval==1:return(rlist)
					
		return(None)
	
	#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
	#CHECK NEIGHBORHOOD
	#NOTE: still not chaining adjacent eqns...might leave off for now.
	#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
	def check_neighborhood(self,rlist):
		board_map=self.board_map
		M=self.M
		N=self.N
		
		ok=1
		slen=len(rlist)
		head=(rlist[0][1],rlist[0][2])
		tail=(rlist[slen-1][1],rlist[slen-1][2])
		if rlist[0][2]==rlist[1][2]:
			iscol=1
			col=rlist[0][2]
		else:
			iscol=0
			row=rlist[0][1]
		
		if iscol:
			#check above:
			if head[0]==0:pass
			elif board_map[head[0]-1][col]!='':ok=-1;return(ok)
			else:pass
			#check below:
			if tail[0]==M-1:pass
			elif board_map[tail[0]+1][col]!='':ok=-2;return(ok)
			else:pass
			#check left:
			if col==0:pass
			else:
				#for ridx in range(head[0],tail[0]):
				for qty in rlist:
					if qty[0][:3]=='WC:':pass
					elif board_map[qty[1]][col-1]!='':ok=-3;return(ok)
			#check right:
			if col==N-1:pass
			else:
				#for ridx in range(head[0],tail[0]):
				for qty in rlist:
					if qty[0][:3]=='WC:':pass
					elif board_map[qty[1]][col+1]!='':ok=-4;return(ok)
			
		else:#submission is a row
			#check left:
			if head[1]==0:pass
			elif board_map[row][head[1]-1]!='':ok=-5;return(ok)
			else:pass
			#check right:
			if tail[1]==N-1:pass
			elif board_map[row][tail[1]+1]!='':ok=-6;return(ok)
			else:pass
			#check above:
			if row==0:pass
			else:
				#for cidx in range(head[1],tail[1]):
				for qty in rlist:
					if qty[0][:3]=='WC:':pass
					elif board_map[row-1][qty[2]]!='':ok=-7;return(ok)
			#check below:
			if head[0]==M-1:pass
			else:
				#for cidx in range(head[1],tail[1]):
				for qty in rlist:
					if qty[0][:3]=='WC:':pass
					elif board_map[row+1][qty[2]]!='':ok=-8;return(ok)
		return(ok)
