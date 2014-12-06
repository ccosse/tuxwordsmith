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

import os, pygame
from pygame.locals import *
import string,math

DEBUG=0

class TWS_Validator:
	"""Validator has game model.
	
	"""
	def __init__(self,board,game):
		self.board=board
		self.game=game
		
	def validate(self,submission):
		if len(submission)==0:return(0)
		board=self.board
		if DEBUG:print submission
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#need to find head,row,col,len and set spot variables accordingly:
		
		MinM=board.M;MinN=board.N
		
		#this handles row/col both:(we want smallest M,N)
		for spot in submission:
			if spot.M<=MinM and spot.N<=MinN:
				MinM=spot.M
				MinN=spot.N
		#print 'preliminary: MinM,MinN=',MinM,MinN
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#Check if anything to LHS or Above
		try_above=1
		#LHS
		while 1:
			if MinN==0:break
			elif board.get_spotMN(MinM,MinN-1).guest !=None:
				MinN=MinN-1
				try_above=0
			else:break
		#Above:
		while 1:
			if not try_above:break
			elif MinM==0:break
			elif board.get_spotMN(MinM-1,MinN).guest !=None:
				MinM=MinM-1
			else:break
		#print 'final MinM,MinN=',MinM,MinN
			
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#Get MaxM,N of submission (so can check RHS and Below):
		
		MaxM=0;MaxN=0
	
		#this handles row/col both:(we want largest M,N)
		for spot in submission:
			if spot.M>=MaxM and spot.N>=MaxN:
				MaxM=spot.M
				MaxN=spot.N
		#print 'preliminary: MaxM,MaxN=',MaxM,MaxN
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#*************NOTE: MaxM,N possible=board.M-1,N-1******************
		#Check if anything to RHS or Below
		#RHS:
		try_below=1
		while 1:
			#print 'checking RHS: MaxM,MaxN,board.M,N=',MaxM,MaxN,board.M,board.N
			if MaxN==board.N-1:break
			elif board.get_spotMN(MaxM,MaxN+1).guest !=None:
				MaxN=MaxN+1
				try_below=0
			else:break
		#Below:
		while 1:
			#print 'checking Below: MaxM,MaxN,board.M,N=',MaxM,MaxN,board.M,board.N
			if not try_below:break
			elif MaxM==board.M-1 :break
			elif board.get_spotMN(MaxM+1,MaxN).guest !=None:
				MaxM=MaxM+1
			else:break
		#print 'final MaxM,MaxN=',MaxM,MaxN
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#can put exprtype determination here, no?
		if MaxM-MinM>0 and MaxN-MinN>0:return(0)#can't be both types
		elif MaxM-MinM>0:exprtype='col'
		elif MaxN-MinN>0:exprtype='row'
		elif MaxN-MinN==0:
			#print 'That\'s Not An Equation!'
			return(0)
		else:
			#print 'THIS SHOULD NOT HAPPEN(and this else clause should be able to be removed)!!!!!!!!!!!'
			return(0)
		#print 'exprtype=',exprtype
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#Check continuous between Min/Max
		if exprtype=='row':
			#print 'row row row row row row row'
			for idx in range(MinN,MaxN+1):
				this_idx_okay=0
				#print ' idx=',idx,
				#one of either (submission[*].N==idx) or (board[Min/MaxM][idx].guest !=None) must be true:
				for spot in submission:
					if spot.N==idx:this_idx_okay=1
				if board.get_spotMN(MinM,idx).guest!=None:this_idx_okay=1
				if this_idx_okay==0:
					#print 'ROWGAPROWGAPROWGAPROWGAPROWGAPROWGAPROWGAPROWGAP: ->',idx
					return(0)
				
		elif exprtype=='col':
			#print 'col col col col col col col'
			for idx in range(MinM,MaxM+1):
				this_idx_okay=0
				#print ' idx=',idx,
				#one of either (submission[*].N==idx) or (board[Min/MaxM][idx].guest !=None) must be true:
				for spot in submission:
					if spot.M==idx:this_idx_okay=1
				if board.get_spotMN(idx,MinN).guest!=None:this_idx_okay=1
				if this_idx_okay==0:
					#print 'COLGAPCOLGAPCOLGAPCOLGAPCOLGAPCOLGAPCOLGAPCOLGAP: ->',idx
					return(0)
			
		"""
		At this point, if this_idx_okay==0 then we can throw submission back -> tray because you can't
		do two separate equations in a turn. One point that we might ought to have handled already: What
		if the submission involved a row and a column? (Can't think of example where possible, but not 
		sure its not) Hence above "if not valid, return(0)". Okay, i guess the gut-feelings i'm having
		that such cases exist are if we enter something into a corner (which would necessarily be an
		equal sign!), but would then be working 2 equations at once -- what was decided not to support,
		at least at first.
		"""
		
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#Build the expression -> string
		expr=''
		if exprtype=='row':
			for idx in range(MinN,MaxN+1):
				if board.get_spotMN(MinM,idx).guest!=None:
					expr=expr+board.get_spotMN(MinM,idx).guest.str_val
					continue
				else:
					for spot in submission:
						if spot.N==idx:
							expr=expr+spot.guest.str_val
							continue
		elif exprtype=='col':
			for idx in range(MinM,MaxM+1):
				if board.get_spotMN(idx,MinN).guest!=None:
					expr=expr+board.get_spotMN(idx,MinN).guest.str_val
					#continue
				else:
					for spot in submission:
						if spot.M==idx:
							#print 'requesting idx,MinN=',idx,MinN
							expr=expr+spot.guest.str_val
							#continue
		
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		
		#perform some basic sanity checks:
		
		if expr.count('=')==0:
			if DEBUG:print 'bailing because no = sign found'
			return(0)
		
		#revised implementation to handle 0-99:
		length=len(expr)
		for twodigitnum in range(10,100):
			length-=expr.count(unicode(twodigitnum))
		if math.fmod(length,2)==0:
			print 'my new function says NO'
			return(0)
		
		
		#alternating ops, no first/last opps
		#commenting-out this section: still fails to evaluate, so okay.
		"""
		list_expr=list(expr)
		ops=['+','-','*','/','=']
		should_be_op=0
		for idx in range(len(list_expr)):
			if should_be_op==0:
				try:rval=eval(list_expr[idx])
				except:
					print 'bail 1'
					return(0)
			else:
				if ops.count(list_expr[idx])==0:
					print 'bail 2'
					return(0)
			if should_be_op==0:should_be_op=1
			else:should_be_op=0
		"""
		
		expr=expr.replace('=','==')#last step before evaluating!
		
		#evaluate it:
		#print 'EXPRESSION=',expr
		try:rval=eval(expr)
		except:return(0)
		if rval==0:return(0)
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		head_spot=None
		for spot in submission:#was head in submission?
			if spot.M==MinM and spot.N==MinN:head_spot=spot
		if not head_spot:#then head must have been on board.
			head_spot=board.get_spotMN(MinM,MinN)
				
		head_spot.AMHEAD=1
		if exprtype=='row':
			head_spot.AMROWEXPR=1
			head_spot.ROWEXPRLENGTH=MaxN-MinN+1
		if exprtype=='col':
			head_spot.AMCOLEXPR=1
			head_spot.COLEXPRLENGTH=MaxM-MinM+1
		
		#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
		#did this submission affect any HEADS in it's range? Check-and-update!
		
		addition_used=0
		subtraction_used=0
		multiplication_used=0
		division_used=0
				
		if exprtype=='row':
			multiplier=1
			score=0
			
			#This gives points for newly submitted tiles:
			for sidx in range(len(submission)):
				try:
					score+=submission[sidx].guest.ptval
					
				except Exception,e:
					if DEBUG:print e
			
			#This gives points for pieces already on board:
			for nidx in range(MinN,MaxN+1):
				spot2check=board.get_spotMN(MinM,nidx)
				try:
					ptval=spot2check.guest.ptval
					score+=ptval
					self.game.num_replacements+=1
					
				except Exception,e:
					if DEBUG:print e
				
			
			
			self.game.players[self.game.player_idx].score+=score
			self.game.last_points=score
			
			for n in range(MinN+1,MaxN+1):#don't overwrite new head (hence * MinN+1 *)
				#only bother if on board
				if board.check4guest(MinM,n):
					spot2check=board.get_spotMN(MinM,n)
					
					if spot2check.AMHEAD and spot2check.AMROWEXPR:
						spot2check.AMROWEXPR=0
						spot2check.ROWEXPRLENGTH=0
						#if also COLHEAD then don't unset AMHEAD, else do!
						if spot2check.AMCOLEXPR:pass
						else:spot2check.AMHEAD=0
			
						
		if exprtype=='col':
			multiplier=1
			score=0
			
			#This gives points for newly submitted tiles:
			for sidx in range(len(submission)):
				try:
					score+=submission[sidx].guest.ptval

				except Exception,e:
					if DEBUG:print e
					
			
			#This gives points for pieces already on board:
			for midx in range(MinM,MaxM+1):
				spot2check=board.get_spotMN(midx,MinN)
				try:
					ptval=spot2check.guest.ptval
					score+=ptval
					self.game.num_replacements+=1

				except Exception,e:
					if DEBUG:print e
			
					
			self.game.players[self.game.player_idx].score+=score
			self.game.last_points=score
			
			for m in range(MinM+1,MaxM+1):#don't overwrite new head (hence * MinN+1 *)
				#only bother if on board
				if board.check4guest(m,MinN):
					spot2check=board.get_spotMN(m,MinN)
					
					if spot2check.AMHEAD and spot2check.AMCOLEXPR:
						spot2check.AMCOLEXPR=0
						spot2check.COLEXPRLENGTH=0
						#if also ROWHEAD then don't unset AMHEAD, else do!
						if spot2check.AMROWEXPR:pass
						else:spot2check.AMHEAD=0
		
		return(1)
