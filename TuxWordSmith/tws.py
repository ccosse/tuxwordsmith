#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
from random import *


import pygame
from pygame.locals import *

from twssolver import *
from twslocalizer import *
from twsvalidator import *
from button import *
from round_button import *
from player import *
from board import *
from spot import *
from tile import *
from actor import *
from environment import *
from dict_formatter import *
from projectile import *

DEBUG=0

global images
images={}

class TuxWordSmithApp:
	
	def __init__(self):
		
		mode=0#-1,0,1,2 = quit/screensaver/play/admin
		level=4
		use_default_level=True
		
		while True:
			
			prog=TuxWordSmith(mode,level,use_default_level,False)
			#rval=prog.admin.ShowModal()
			#sys.exit()
			mode,level=prog.run()
			
			
			if mode<0:prog.on_exit()
			elif mode==0:pass#prog.update_highscores()
			elif mode==1:prog.update_highscores()
			elif mode==2:
				#rval=prog.admin.ShowModal()
				mode=0
			else: mode=0
			
			use_default_level=0
			
			
class TuxWordSmith(TWSSolver):
	
	global images
	
	def __init__(self,mode,level,use_default_level,USE_WX):
	
		if USE_WX:
			import wxadmin
			from wxadmin import wxAdmin
		
		TWSSolver.__init__(self,mode,level)
		
		self.player_idx=0
		
		self.W=None
		self.H=None
		self.y00=None
		self.bkg=None
		self.bgImage=None
		self.screen=None
		
		self.CANNOT_MOVE_COUNT=0
		self.AMFULLSCREEN=0
		self.MOVIE=0
		
		self.bfont=None
		self.cfont=None
		self.pfont=None
		self.hudfont=None
		self.overlayfont=None
		self.overlayfont_small=None
		self.appnamefont=None
		self.myfont_large=None
		self.myfont_medium=None
		self.myfont_small=None
		self.myfont_xsmall=None
		
		self.submission=None
		self.highscore_surface=None
		self.current_resource_surface=None
		
		self.admin_button=None
		self.demo_button=None
		self.play_button=None
		self.quit_button=None
		self.skip_button=None
		self.okay_button=None
		
		self.adminbuttongroup=None
		self.adminbuttons=None
		
		self.playbuttongroup=None
		self.playbuttons=None
		
		self.demobuttongroup=None
		self.demobuttons=None
		
		self.quitbuttongroup=None
		self.quitbuttons=None
		
		self.skipbuttongroup=None
		self.skipbuttons=None
		
		self.okaybuttongroup=None
		self.okaybuttons=None
		
		self.board=None
		self.boardspots=None
		self.AnimatedTiles=[]
		self.submission=None
		self.submissionspots=None
		self.solver_submission=[]
		
		self.pickup_sounds	=None
		self.release_sounds	=None
		self.lockin_sounds	=None
		self.bounce_sounds	=None
		self.lose_sounds	=None
		self.win_sounds		=None

		self.admin=None
		self.player_idx=0
		self.target=None
		self.players=[]
		self.tray_spots=[]
		self.t_last=time.time()
		self.animation_in_progress=0
		
		self.last_defn=None
		self.last_str_defn=""
		
		self.env=Environment('TuxWordSmith')
		self.env.USE_WX=False
		if USE_WX:self.env.USE_WX=USE_WX

		self.STOP_RUNNING=0
		self.CANNOT_MOVE_COUNT=0
		
		if self.env.OS=="win":
			os.environ['SDL_VIDEODRIVER'] = 'windib'
		pygame.display.init()
		pygame.init()
		
		pygame.event.set_blocked(MOUSEMOTION)#Wow! this helps!

		self.global_config=self.load_config()
		if sys.argv.count("-d")>0:
			didx=sys.argv.index("-d")
			dictionary_resource=sys.argv[didx+1]
			self.global_config['DICTIONARY_RESOURCE']['value']=dictionary_resource
		
		pygame.display.set_caption(self.global_config['APPNAME'])
		self.target=pygame.sprite.RenderClear()#drag-n-drop object
		
		self.admin=None
		if self.env.USE_WX:
			self.admin=wxAdmin(self)
			self.admin.setup()
		
		self.bag_of_tiles=[]

		if use_default_level:self.LEVEL=self.global_config['DEFAULT_LEVEL']['value']
		
		self.tiledir=os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Tiles')
		self.SCREENSAVER=self.global_config['SCREENSAVER_ON_AT_START']['value']

		self.clock = pygame.time.Clock()

	def handle_mouse(self):	
		#for event in pygame.event.get():
		#	print event
			
		for event in pygame.event.get(MOUSEBUTTONDOWN):
			
			#DEMO BUTTON:
			if self.demo_button.rect.collidepoint(pygame.mouse.get_pos()):
				self.STOP_RUNNING=0
				self.MODE=0
				return 1

			#LOGIN/LOGOUT BUTTON:
			if self.play_button.rect.collidepoint(pygame.mouse.get_pos()):
				self.STOP_RUNNING=0
				self.MODE=1
				return 1
				
			if self.quit_button.rect.collidepoint(pygame.mouse.get_pos()):
				self.STOP_RUNNING=1
				sys.exit()

			#ADMIN BUTTON:
			elif self.admin_button.rect.collidepoint(pygame.mouse.get_pos()):
				self.AMFULLSCREEN=0
				self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
				#self.animation_in_progress=0
				self.MODE=2
				self.STOP_RUNNING=1
				return 1
				
			if self.MODE==0:return 0

		for event in pygame.event.get(QUIT):
			pygame.quit()
			sys.exit()
		
				
	def refill_bag_of_tiles(self):
		gc=self.global_config
		letters=gc['letters']
		distribution=gc['distribution']
		tile_size=gc['TILESIZE']['value']
		
		if 1:#DEBUG:
			if DEBUG:
				print 'gc[scoring]=',gc['scoring']
				for key in distribution.keys():
					if DEBUG:pass
					if DEBUG:print "%30s\t%02d"%(key,distribution[key])
					print key,' distribution[key]=',distribution[key]
			if DEBUG:
				print letters
				keys=gc['scoring'].keys()
				for idx in range(len(keys)):
					print keys[idx],gc['scoring'][keys[idx]]
				#sys.exit()
				
		for idx in range(len(letters)):
			
			uchar=letters[idx]
			uname=unicodedata.name(uchar)
			ptval=gc['scoring'][uname]
			ncopy=max(1,distribution[uname])
			
			if 1:#DEBUG:
				if DEBUG:print "ncopy=%d\t%s"%(ncopy,uname)
			
			for dummy in range(ncopy):
				
				img=pygame.Surface((tile_size,tile_size))
				tile=Tile(img,idx,uname,uchar,ptval)
				self.bag_of_tiles.append(tile)
		
		#Shuffle
		if DEBUG:print 'shuffling...'
		for nshuffle in range(1000*len(gc['letters'])):
			tile=self.bag_of_tiles.pop()
			idx2insert=int(random()*len(self.bag_of_tiles))
			self.bag_of_tiles.insert(idx2insert,tile)
		if DEBUG:print 'finished shuffling'
		
	
	def draw_tiles(self):
		gc=self.global_config
		spots=self.players[self.player_idx].tray.get_spots()
		
		for spot in spots:
			
			if len(self.bag_of_tiles)==0:
				self.refill_bag_of_tiles()
			
			if spot.occupied():continue
			
			#number,strval,ptval=self.draw_number_strval_ptval()
			#uchar=number
			#tile=self.make_tile(strval,uchar,ptval)
			
			tile_size=gc['TILESIZE']['value']
			tile=self.bag_of_tiles.pop()
			tile.image.fill((0,0,0))
			white_border=pygame.Surface((tile_size-2,tile_size-2))
			white_border.fill((255,255,255))
			tile.image.blit(white_border,(1,1))
			black_rect=pygame.Surface((tile_size-4,tile_size-4))
			black_rect.fill((0,0,0))
			tile.image.blit(black_rect,(2,2))
			
			font_surface=None
			ptval_surface=None
			
			if gc['TILES_TWO_COLORS']['value']==1 and self.player_idx==1:
				font_rect=pygame.Surface((tile_size-6,tile_size-6))
				font_rect.fill((gc['COLOR_BG_PLAYER1_TILE']['value']))
				tile.image.blit(font_rect,(3,3))
				font_surface=self.cfont.render(tile.uchar,1,gc['COLOR_FG_PLAYER1_TILE']['value'],gc['COLOR_BG_PLAYER1_TILE']['value'])
				ptval_surface=self.pfont.render(`tile.ptval`,1,gc['COLOR_FG_PLAYER1_TILE']['value'],gc['COLOR_BG_PLAYER1_TILE']['value'])
			
			else:
				
				font_rect=pygame.Surface((tile_size-6,tile_size-6))
				font_rect.fill((gc['COLOR_BG_PLAYER0_TILE']['value']))
				tile.image.blit(font_rect,(3,3))
				font_surface=self.cfont.render(tile.uchar,1,gc['COLOR_FG_PLAYER0_TILE']['value'],gc['COLOR_BG_PLAYER0_TILE']['value'])
				ptval_surface=self.pfont.render(`tile.ptval`,1,gc['COLOR_FG_PLAYER0_TILE']['value'],gc['COLOR_BG_PLAYER0_TILE']['value'])
			
			
			tlcx=tlcy=None	
			if 0:#self.env.OS=='win':
				tlcx=tile_size/2-font_surface.get_width()/2+2
				tlcy=tile_size/2-font_surface.get_height()/2
			else:
				tlcx=tile_size/2-font_surface.get_width()/2-2
				tlcy=tile_size/2-font_surface.get_height()/2-1
			
			tile.image.blit(font_surface,(tlcx,tlcy))
				
			tlcx=tile_size-ptval_surface.get_width()-4
			tlcy=tile_size-ptval_surface.get_height()-3
			
			if gc['TILE_SHOW_VALUE']['value']==1:
				tile.image.blit(ptval_surface,(tlcx,tlcy))
			
			tile.image.set_alpha(gc['COLOR_TILE_ALPHA']['value'])
			
			spot.take_guest(tile,1)
			tile.saved_center=spot.rect.center
			
		
	def skip_turn(self):
		self.throw_back_submission()
		self.players[self.player_idx].actor.queue('go_back')
		self.increment_player_idx()
		self.CANNOT_MOVE_COUNT+=1
		
	def exchange(self):
		if DEBUG:print 'K_F8: exchange'
		self.throw_back_submission()
		#complete replacement (for ease of coding)
		spots=self.players[self.player_idx].tray.get_spots()
		for spot in spots:
			self.bag_of_tiles.insert(int(random()*len(self.bag_of_tiles)),spot.pop_guest())
		self.draw_tiles()
		self.players[self.player_idx].actor.queue('go_back')
		self.increment_player_idx()
		self.players[self.player_idx].actor.queue('get_up')
		self.CANNOT_MOVE_COUNT+=1
		
	def increment_level(self):
		self.LEVEL+=1
		if self.LEVEL>4:self.LEVEL=1

	def timer_update(self):
		t_current=time.time()
		self.dt_last=t_current-self.t_last
		self.t_last=t_current
		return self.dt_last
		
	def increment_player_idx(self):
		dt_last=self.timer_update()
		if DEBUG:print dt_last,self.players[0].score,self.players[1].score
		self.player_idx+=1
		if self.player_idx>1:self.player_idx=0
		if DEBUG:print 'increment_player_idx:',self.player_idx
		
		
	def shuffle(self):
		if DEBUG:print 'K_F5: shuffle'
		self.throw_back_submission()
		self.submissionspots.empty()
		glyphs=[]
		spots=self.players[self.player_idx].tray.get_spots()
		for spot in spots:
			glyphs.append(spot.pop_guest())
		
		#shuffle the lists, then put back in order:
		for dummy in range(10):
			glyph=glyphs.pop()
			nidx=int(random()*len(glyphs))
			glyphs.insert(nidx,glyph)

		#now put back sequentially:
		for spot in spots:
			glyph=glyphs.pop()
			glyph.saved_center=spot.rect.center
			spot.take_guest(glyph,1)
			
			
	def create_default_spot_surface(self,visible):
		dx=dy=self.global_config['TILESIZE']['value']
		surf=pygame.Surface((dx,dy))
		bgcolor=self.global_config['COLOR_BG']['value']
		spot_color=self.global_config['COLOR_SPOT']['value']
		surf.fill(bgcolor)
		
		if visible:
			fgsurf=pygame.Surface((dx-4,dy-4))
			fgsurf.fill(spot_color)
			surf.blit(fgsurf,(2,2))
			
			fgsurf=pygame.Surface((dx-8,dy-8))
			fgsurf.fill(bgcolor)
			surf.blit(fgsurf,(4,4))
		
		surf.set_colorkey(bgcolor)
		surf.set_alpha(self.global_config['COLOR_SPOT_ALPHA']['value'])
		return surf
	
	def end_of_game_reached(self):
		if DEBUG:print 'END OF GAME REACHED'
	
	def run(self):
		#print 'run MODE=',self.MODE
		if DEBUG:print 'run calling update'
		
		self.update_global_config_dependents()#move dictionary stuff to after splash!!!
		if self.MODE==0:self.go_splash()
		if self.MODE==2:
			return self.MODE,self.LEVEL
			
		self.load_resources()
		
		for self.player_idx in range(2):self.draw_tiles()
		
		while not self.STOP_RUNNING:
			#if DEBUG:print 'player_idx=',self.player_idx,self.players[self.player_idx].mode,self.MODE
			if self.CANNOT_MOVE_COUNT>=self.global_config['END_GAME_THRESHOLD']['value']:
				self.end_of_game_reached();break
			if DEBUG:print 'calling take_turn...'
			self.take_turn()
			if DEBUG:print 'calling update...'
			self.update()
			if DEBUG:print 'looping...'
			
		return self.MODE,self.LEVEL
	
	def busy(self):
		
		for pidx in range(2):
			if len(self.players[pidx].actor.maneuver_queue):return 1
		
		if self.animation_in_progress:return 1
		
		return 0
		
	def take_turn(self):
		if self.players[self.player_idx].mode==1:return
		if self.STOP_RUNNING:return
		
		if DEBUG:print '\n\n*****************'
		if DEBUG:print 'take_turn'
		if DEBUG:print 'player_idx=',self.player_idx
		if DEBUG:print 'entering update loop...'
		self.update()
		while self.busy():
			self.update()
			if self.STOP_RUNNING==1:return
		if DEBUG:print 'done'
		
		#self.players[self.player_idx].solver.generate_expressions(1.0)
		
		#if DEBUG:print 'calling generate options\n',self.player_idx,'\n',self.solver_submission,'\n',self.players
		
		self.solver_submission,self.last_str_defn=self.players[self.player_idx].solver.generate_options()#solver sets num_replacements
		self.set_last_defn(self.last_str_defn)
		rlist=self.solver_submission
		
		if rlist:
			
			if DEBUG:print 'yes rlist'
			
			if len(rlist)==self.NTRAYSPOTS:
				#NEED: Flashing Award Notification 
				self.players[self.player_idx].score+=self.global_config['BONUS_FOR_USING_ALL_TILES']['value']
				
				
			for idx in range(len(rlist)):
				tile=self.players[self.player_idx].tray.get_guest_by_str(rlist[idx][0])
				spot=self.submission.take_guestMN(tile,rlist[idx][1],rlist[idx][2])
				self.submissionspots.add(spot)
				
				startpos=tile.saved_center
				endpos=spot.rect.center
				DX=float(endpos[0]-startpos[0])
				DY=float(startpos[1]-endpos[1])
				
				theta=None
				if DX==0 and DY>=0:theta=math.pi/2.
				elif DX==0 and DY<0:theta=-math.pi/2.
				else:
					theta0=math.atan(abs(DY)/abs(DX))
					if DX>=0 and DY>=0:theta=theta0
					elif DX<=0 and DY>=0:theta = math.pi-theta0
					elif DX<=0 and DY<=0:theta = math.pi+theta0
					elif DX>=0 and DY<=0:theta = -1.*theta0
				
				STEPSIZE=self.global_config['TILE_ANIM_STEPSIZE']['value']
				dx=STEPSIZE*math.cos(theta)
				dy=-STEPSIZE*math.sin(theta)
				
				spot.rect.center=startpos
				xc=startpos[0]
				yc=startpos[1]
				while not spot.rect.collidepoint(endpos):
					xc+=dx
					yc+=dy
					spot.rect.center=(int(xc),int(yc))
					#print startpos,endpos,DX,DY,theta0*180./math.pi,theta*180./math.pi,spot.rect.center,xc,yc
					
					if self.STOP_RUNNING:return
					self.update()
					self.handle_events()
					
				spot.rect.center=endpos
			self.board.increment_num_commited()
			self.CANNOT_MOVE_COUNT=0
			
			self.players[self.player_idx].actor.queue('celebrate');
			self.players[self.waiting_player_idx()].actor.queue('get_tougher')

		
		else:
			if DEBUG:print 'no rlist'
			#self.exchange()
			spots=self.players[self.player_idx].tray.get_spots()
			for spot in spots:
				self.bag_of_tiles.insert(0,spot.pop_guest())
			self.CANNOT_MOVE_COUNT+=1
		
		for spot in self.submissionspots.sprites():
			for board_spot in self.board.get_spots():
				if board_spot.rect.center==spot.rect.center:# M,N-Matching
					tile=None
					tile=spot.pop_guest()
					self.submission.remove(spot)
					if tile:
						board_spot.take_guest(tile,1)
						board_spot.msg=self.last_str_defn
						board_spot.lock()
						if self.global_config['TILE_ANIMATIONS']['value']==1:
							self.AnimatedTiles[board_spot.getMN()[0]][board_spot.getMN()[1]].queue('celebrate')
						
		self.players[self.player_idx].actor.queue('go_back')
		self.players[self.waiting_player_idx()].actor.queue('get_up')
		
		self.submissionspots.empty()
		self.draw_tiles()
		self.handle_events()
		self.update()
		self.increment_player_idx()
		
		if DEBUG:print 'finished taking turn'
		
		
	def waiting_player_idx(self):
		waiting_player_idx=0
		if self.player_idx==0:waiting_player_idx=1
		return waiting_player_idx

	def handle_events(self):
		
		for event in pygame.event.get(QUIT):
			pygame.quit()
			sys.exit()
		
		for e in pygame.event.get():
			
			#################################
			if e.type==KEYDOWN:
				
				if e.key==K_ESCAPE:
					self.STOP_RUNNING=1
					if self.MODE>0:self.MODE-=1#this backs-you-out of mode-levels, escaping each successive
					return
					
				elif e.key==K_F1:
					self.set_last_defn('')
					
				elif e.key==K_F2:
					self.focus_definition()

				elif e.key==K_F3:
					self.MOVIE+=1
					if self.MOVIE>1:self.MOVIE=0
				
				elif e.key==K_F4:
					self.players[0].set_mode(0)
					self.players[1].set_mode(0)
					self.LEVEL=self.global_config['DEFAULT_LEVEL']['value']
					self.STOP_RUNNING=1
					self.MODE=0
					
				elif e.key==K_F5:self.shuffle()#shuffle numbers by: first pop from spot, then re-parent
				
				elif e.key==K_F7:	
					self.throw_back_submission()
					self.submissionspots.empty()
					
				elif e.key==K_F8:
					if self.MODE==0:continue
					self.exchange()#exchange tiles which have been dragged to board (ie are thereby regarded by game as a submission)
				
				elif e.key==K_F9:self.go_help()
				elif e.key==K_F10:self.go_credit()
				elif e.key==K_F11:self.go_screenshot()
				elif e.key==K_F12:self.go_fullscreen()
				
			#################################
			if e.type == MOUSEBUTTONDOWN:
				
				#print e.dict
				
				#CHECK FOR RIGHT MOUSE:
				if e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]==1:#right-mouse; will probably crash on Mac mouse
					
					all_spots=self.players[0].tray.get_spots()
					all_spots+=self.players[1].tray.get_spots()
					all_spots+=self.board.get_spots()
					all_spots+=self.submission.get_spots()
					SHOW_DISTRIBUTION_FLAG=1
					for spot in all_spots:
						if spot.rect.collidepoint(pygame.mouse.get_pos()) and spot.occupied():
							self.show_letter_overlay(spot)
							SHOW_DISTRIBUTION_FLAG=0
					
					if SHOW_DISTRIBUTION_FLAG:self.show_dist_overlay()
				
				elif e.type == MOUSEBUTTONDOWN and e.dict['button']>3:#scroll wheel
					self.shuffle()
					
				#NEW FEATURE: 10-08-2007
				elif e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]==0:
					found=0
					for spot in self.board.get_spots():
						if spot.rect.collidepoint(pygame.mouse.get_pos()) and spot.islocked():
							self.show_defn_overlay(spot)
							found=1
							
					#10-25-2008 clear defn if click on background
					if not found:self.set_last_defn('')
				
				
				if self.MODE==0:return
				
				elif self.okay_button.rect.collidepoint(pygame.mouse.get_pos()) and self.MODE==1:
					
					#if(self.validator.validate(self.submissionspots.sprites())):#ready for this now!(first player turn)
					if(self.validate(self.submissionspots.sprites())):
						
						#NEED:blackjack-style bonus alert
						if len(self.submissionspots.sprites())==self.NTRAYSPOTS:
							self.players[self.player_idx].score+=self.global_config['BONUS_FOR_USING_ALL_TILES']['value']
							
						if self.global_config['SOUNDON']['value']:
							coin=int(random()*len(self.win_sounds))
							self.win_sounds[coin].play()
							
						self.CANNOT_MOVE_COUNT=0
						self.board.increment_num_commited()
						
						for spot in self.submissionspots.sprites():
							for board_spot in self.board.get_spots():
								if board_spot.rect.center==spot.rect.center and spot.guest:
									#validator is gonna have to fill-in AMHEAD fields, then add->board.list_of_heads.add(spot)
									#print spot.guest.str_val,'len=',len(board.get_spots()),len(submissionspots.sprites())
									tile=spot.pop_guest()
									
									#while we've got spot center info set_center of cuckoo_tile:
									rect=board_spot.rect
									xc=rect[0]+rect[2]/2
									yc=rect[1]+rect[3]/2
									self.AnimatedTiles[board_spot.getMN()[0]][board_spot.getMN()[1]].queue('celebrate')
									
									#Validator sets submission_spot and game(this) xfers->board_spot; (i.e. they work together)
									if spot.AMHEAD==1:
										board_spot.AMHEAD=1
										if spot.AMROWEXPR==1:
											board_spot.AMROWEXPR=1
											board_spot.ROWEXPRLENGTH=spot.ROWEXPRLENGTH
											
										if spot.AMCOLEXPR==1:
											board_spot.AMCOLEXPR=1
											board_spot.COLEXPRLENGTH=spot.COLEXPRLENGTH
											
									board_spot.take_guest(tile,1)
									board_spot.msg=self.last_str_defn
									board_spot.lock()
									self.submission.remove(spot)
						
						self.draw_tiles()
						self.players[self.player_idx].actor.queue('go_back')
						self.increment_player_idx()
						self.players[self.player_idx].actor.queue('get_up')
						
					
					
					
					else:#put back and play lose sound(not4tux)
						if len(self.players[self.player_idx].actor.maneuver_queue)<2:
							self.players[self.player_idx].actor.queue('incorrect')
							pass
						
						if self.global_config['SOUNDON']['value']:
							if DEBUG:print 'self.global_config[\'SOUNDON\'][\'value\']=',self.global_config['SOUNDON']['value']
							coin=int(random()*len(self.lose_sounds))
							self.lose_sounds[coin].play()
						
					return
				
				
				#CHECK TRAY FOR NEW TARGET:
				for spot in self.players[self.player_idx].tray.get_spots():
					if not spot.guest:continue
					if spot.rect.collidepoint(pygame.mouse.get_pos()):
						
						#NEED: confirm it is player's turn/tray/tile before allowing to move
						
						if self.global_config['SOUNDON']['value']:
							coin=int(random()*len(self.pickup_sounds))
							self.pickup_sounds[coin].play()
						
						self.target.add(spot.pop_guest())
						
				#CHECK THE BOARD FOR NEW TARGET:
				for spot in self.board.get_spots():
					if spot.rect.collidepoint(pygame.mouse.get_pos()) and spot.islocked():
						if self.global_config['SOUNDON']['value']:
							coin=int(random()*len(self.bounce_sounds))
							self.bounce_sounds[coin].play()
						if len(self.players[self.player_idx].actor.maneuver_queue)<2:
							self.players[self.player_idx].actor.queue('incorrect')
						
				#CHECK THE SUBMISSION FOR NEW TARGET:
				#print 'down1:len(submissionspots.sprites())=',len(submissionspots.sprites()),
				for spot in self.submission.get_spots():
					if not spot.occupied():continue
					if len(self.target)==0 and spot.rect.collidepoint(pygame.mouse.get_pos()):
						guest=spot.pop_guest()
						self.submissionspots.remove(spot)
						
						if self.global_config['SOUNDON']['value']:
							coin=int(random()*len(self.pickup_sounds))
							self.pickup_sounds[coin].play()
						
						self.target.add(guest)
			
			#################################
			elif e.type == MOUSEBUTTONUP:
				if len(self.target.sprites())>0:
					for spot in self.submission.get_spots():
						if spot.rect.collidepoint(self.target.sprites()[0].rect.center):#welcome to new home
							#print 'up1:len(submissionspots.sprites())=',len(submissionspots.sprites()),
							if spot.occupied():continue#part of submission
							#elif spot.islocked():continue#part of board
							spot.take_guest(self.target.sprites()[0],1)
							
							if self.global_config['SOUNDON']['value']:
								coin=int(random()*len(self.lockin_sounds))
								self.lockin_sounds[coin].play()
							
							self.submissionspots.add(spot)
							self.target.empty()
							
							return
					
					if len(self.target.sprites())==0:continue
					
					for spot in self.board.get_spots():
						if spot.rect.collidepoint(self.target.sprites()[0].rect.center):	
							
							if self.global_config['SOUNDON']['value']:
								coin=int(random()*len(self.bounce_sounds))
								self.bounce_sounds[coin].play()
								
							if len(self.players[self.player_idx].actor.maneuver_queue)<2:
								self.players[self.player_idx].actor.queue('incorrect')
								
							return
							
					if len(self.target.sprites())>0:#didn't drop? revert!
						tile=self.target.sprites()[0]
						self.target.remove(tile)
						for spot in self.players[self.player_idx].tray.get_spots():	
							if tile.saved_center==spot.rect.center:
								spot.take_guest(tile,1)
								return
					

	def throw_back_submission(self):
		
		for spot in self.submissionspots.sprites():#reset
			tile=spot.pop_guest()
			if tile:
				for spot in self.players[self.player_idx].tray.get_spots():	
					if	tile.saved_center==spot.rect.center:
						spot.take_guest(tile,1)
		
		while len(self.target.sprites())>0:
			tile=self.target.sprites()[0]
			self.target.remove(tile)
			for spot in self.players[self.player_idx].tray.get_spots():	
				if tile.saved_center==spot.rect.center:
					spot.take_guest(tile,1)
	
	
	def update(self):
		#print 'self.global_config[\'SOUNDON\'][\'value\']=',self.global_config['SOUNDON']['value']
		if DEBUG:print 'update -> handle_events'	
		if self.STOP_RUNNING==1:return
		self.handle_events()
		if self.STOP_RUNNING==1:return
		

		self.clock.tick(80)

		if time.time()-self.t_last>0.05:
			#print 'dt=',time.time()-self.t_last
			pass
		elif (self.animation_in_progress==1 and time.time()-self.t_last>self.players[0].actor.dt):
			#print 'animating'
			pass
		else:
			#print 'skip'
			return

		self.t_last=time.time()

		waiting_player_idx=0
		if self.player_idx==0:waiting_player_idx=1
		self.players[waiting_player_idx].wait_counter+=1
		if self.players[waiting_player_idx].wait_counter>=self.global_config['PLAYER_WAIT_COUNTER']['value']:
			self.players[waiting_player_idx].actor.queue('waiting')
			self.players[waiting_player_idx].wait_counter=0
		
		self.screen.blit(self.bkg,(0,0))
		if self.bgImage:
			self.screen.blit(self.bgImage,(0,0))
		
		self.boardspots.draw(self.screen)
		self.submissionspots.draw(self.screen)
		for idx in range(2):self.tray_spots[idx].draw(self.screen)
		
		"""
		#BUTTONS
		self.adminbuttons.draw(self.screen)
		"""
		if self.MODE==0:pass#self.playbuttons.draw(self.screen)
		else:self.quitbuttons.draw(self.screen)
		
		#CURRENT_RESOURCE
		sw=self.current_resource_surface.get_width()
		xc=self.global_config['WIN_W']['value']/2
		self.screen.blit(
			self.current_resource_surface,
			((xc-sw/2),self.global_config['WIN_H']['value']-25)
		)
		
		"""
		self.draw_feedback_overlay()
		
		#Who's Turn-Indicator:
		XPOS=self.global_config['WIN_W']['value']/2+(self.players[0].tray.N*self.global_config['TILESIZE']['value'])/2
		if self.LEVEL>=3:
			if self.player_idx==0:
				tuxturnstring= "<%s"%(self.global_config['PLAYER_0_CHARACTER']['value'])
				self.screen.blit(self.hudfont.render(tuxturnstring,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value']),(XPOS,40))
			else:
				yourturnstring="<%s"%(self.global_config['PLAYER_1_CHARACTER']['value'])
				self.screen.blit(self.hudfont.render(yourturnstring,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value']),(XPOS,self.global_config['WIN_H']['value']-55))
		else:
			if self.player_idx==0:
				tuxturnstring= "<%s"%(self.global_config['PLAYER_0_CHARACTER']['value'])
				self.screen.blit(self.hudfont.render(tuxturnstring,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value']),(XPOS,40))
			else:
				yourturnstring="<%s"%(self.global_config['PLAYER_1_CHARACTER']['value'])
				self.screen.blit(self.hudfont.render(yourturnstring,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value']),(XPOS,self.global_config['WIN_H']['value']-55))
		"""
		y0=10
		vspc=5
		self.tuxscorestring="Tux:%03d"%self.players[0].score
		surf=self.hudfont.render(self.tuxscorestring,1,self.global_config['COLOR_FG_PLAYER0_TILE']['value'],self.global_config['COLOR_BG']['value'])
		surf.set_colorkey(self.global_config['COLOR_BG']['value'])
		self.screen.blit(surf,(20,y0))
		y0+=surf.get_height()+vspc
		
		self.playerscorestring="You:%03d"%self.players[1].score
		surf=self.hudfont.render(self.playerscorestring,1,self.global_config['COLOR_FG_PLAYER0_TILE']['value'],self.global_config['COLOR_BG']['value'])
		surf.set_colorkey(self.global_config['COLOR_BG']['value'])
		self.screen.blit(surf,(20,y0))
		y0+=surf.get_height()+vspc
		"""
		self.levelstring="Level:%d"%self.LEVEL
		surf=self.hudfont.render(self.levelstring,1,self.global_config['COLOR_BG_PLAYER0_TILE']['value'],self.global_config['COLOR_BG']['value'])
		surf.set_colorkey(self.global_config['COLOR_BG']['value'])
		self.screen.blit(surf,(20,y0))
		y0+=surf.get_height()+vspc
		"""
		self.helpstring="Help:F9"
		surf=self.hudfont.render(self.helpstring,1,self.global_config['COLOR_FG_PLAYER0_TILE']['value'],self.global_config['COLOR_BG']['value'])
		surf.set_colorkey(self.global_config['COLOR_BG']['value'])
		self.screen.blit(surf,(20,y0))
		y0+=surf.get_height()+vspc
		
		
		#LAST DEFINITION:
		#NEED:build this surface 1x and reuse!! duh.
		xc=0
		
		try:
			blc=self.board.get_spotMN(self.global_config['M']['value']-1,0)
			brc=self.board.get_spotMN(self.global_config['M']['value']-1,self.global_config['N']['value']-1)
			x0=blc.rect[0]
			
			#y0=blc.rect[1]+blc.rect[3]+10
			y00=max(self.global_config['WIN_H']['value']/2-self.last_defn_surface.get_height()/2,y0)
			self.y00=y00
			
			x1=brc.rect[0]+brc.rect[2]
			y1=brc.rect[1]+brc.rect[3]+10
			
			xc=self.global_config['WIN_W']['value']/2
			sw=self.last_defn_surface.get_width()
			if self.global_config['AUTO_SHOW_LAST_DEFN']['value']:
				self.screen.blit(self.last_defn_surface,(20,y00))
			
		except Exception,e:
			#print 'could not render defn:',e
			pass

		if self.highscore_surface != None:
			self.screen.blit(self.highscore_surface,(self.global_config['WIN_W']['value']/2-self.highscore_surface.get_width()/2,0))
		
		#Who's Turn-Indicator:
		XPOS=self.global_config['WIN_W']['value']/2+(self.players[0].tray.N*self.global_config['TILESIZE']['value'])/2
		if self.LEVEL>=3:
		   	if self.player_idx==0:
				tuxturnstring= "<-%s"%('Tux')#self.global_config['PLAYER_0_CHARACTER']['value']
				surf=self.hudfont.render(tuxturnstring,1,self.global_config['COLOR_FG_PLAYER0_TILE']['value'],self.global_config['COLOR_BG']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				self.screen.blit(surf,(XPOS,40))
			else:
				yourturnstring="<-%s"%('You')
				surf=self.hudfont.render(yourturnstring,1,self.global_config['COLOR_FG_PLAYER1_TILE']['value'],self.global_config['COLOR_BG']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				self.screen.blit(surf,(XPOS,self.global_config['WIN_H']['value']-55))
		else:
			if self.player_idx==0:
				tuxturnstring= "<-%s"%('Tux')#self.global_config['PLAYER_0_CHARACTER']['value']
				surf=self.hudfont.render(tuxturnstring,1,self.global_config['COLOR_FG_PLAYER0_TILE']['value'],self.global_config['COLOR_BG']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				self.screen.blit(surf,(XPOS,40))
			else:
				yourturnstring="<-%s"%('You')
				surf=self.hudfont.render(yourturnstring,1,self.global_config['COLOR_FG_PLAYER1_TILE']['value'],self.global_config['COLOR_BG']['value'])
				surf.set_colorkey(self.global_config['COLOR_BG']['value'])
				self.screen.blit(surf,(XPOS,self.global_config['WIN_H']['value']-55))
		#####
		
		
		if len(self.target.sprites())>0:
			self.target.sprites()[0].update()
			self.target.draw(self.screen)
		
		#ANIMATED TILE UPDATES:
		t=time.time()
		self.animation_in_progress=0
		for midx in range(len(self.AnimatedTiles)):
			for nidx in range(len(self.AnimatedTiles[0])):
				if self.AnimatedTiles[midx][nidx].xdest or len(self.AnimatedTiles[midx][nidx].maneuver_queue):
					self.AnimatedTiles[midx][nidx].render(t,self.screen,None,None)
					self.animation_in_progress=1
					
		#HIGH_SCORE_LIST:
		#if self.MODE==0 and self.high_score_list:self.blit_high_scores()
		
		#ACTOR UPDATES:
		for plyr in self.players:
			plyr.actor.render(t,self.screen,None,None)
			if plyr.actor.xdest:self.animation_in_progress=1

		#FLIP THE DISPLAY
		self.flip()
		
		if self.MOVIE:
			rval=self.go_screenshot()

	def update_global_config_dependents(self):
		#ie adminbutton which is pygame.sprite.RenderPlain(Group..)
		self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
		self.bkg=pygame.Surface(self.screen.get_size())
		self.bkg=self.bkg.convert()
		self.bkg.fill(self.global_config['COLOR_BG']['value'])
		
		#SET DISPLAY MODE:
		if pygame.display.get_init():
			self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
			self.bkg=pygame.Surface(self.screen.get_size())
			self.bkg=self.bkg.convert()
			self.bkg.fill(self.global_config['COLOR_BG']['value'])
			pygame.font.init()
		
		
		#LOAD FONTS SO CAN DISPLAY PROGRESS MESSAGE:
		self.bfont=pygame.font.Font(
			os.path.join(self.env.configdir,self.global_config['FONT_BFONT']['path'],self.global_config['FONT_BFONT']['value']),
			int(self.global_config['FONTSIZE_BUTTON']['value'])
		)
		self.overlayfont=pygame.font.Font(
			os.path.join(self.env.configdir,self.global_config['FONT_OVERLAY']['path'],self.global_config['FONT_OVERLAY']['value']),
			int(self.global_config['FONTSIZE_OVERLAY']['value'])
			#12
		)
		self.overlayfont_small=pygame.font.Font(
			os.path.join(self.env.configdir,self.global_config['FONT_OVERLAY']['path'],self.global_config['FONT_OVERLAY']['value']),
			int(self.global_config['FONTSIZE_OVERLAY_SMALL']['value'])
			#8
		)
		self.cfont=pygame.font.Font(
			os.path.join(self.env.configdir,self.global_config['FONT_CFONT']['path'],self.global_config['FONT_CFONT']['value']),
			int(self.global_config['FONTSIZE_TILE']['value'])
			#18
		)
		self.pfont=pygame.font.Font(
			os.path.join(self.env.configdir,self.global_config['FONT_PFONT']['path'],self.global_config['FONT_PFONT']['value']),
			int(self.global_config['FONTSIZE_TILE_PTVAL']['value'])
		)
		###
		self.hudfont=pygame.font.Font(
			os.path.join(self.env.configdir,self.global_config['FONT_HUD']['path'],self.global_config['FONT_HUD']['value']),
			int(self.global_config['FONTSIZE_HUD']['value'])
		)
		
		self.appnamefont=pygame.font.Font(
			os.path.join(self.env.configdir,self.global_config['FONT_APPNAME']['path'],self.global_config['FONT_APPNAME']['value']),
			int(self.global_config['FONTSIZE_APPNAME']['value'])
		)
		
		
		#ATTEMPT TO LOAD BGIMAGE:
		if self.global_config['IMAGE_BG']['value']!='':
			try:
				self.bgImage=pygame.image.load(os.path.join(self.global_config['IMAGE_BG']['path'],self.global_config['IMAGE_BG']['value']))#os.path.join(self.sitepkgdir,self.global_config['APPNAME'],'Images','sunset01.jpg')
				self.bgImage=pygame.transform.scale(self.bgImage, (self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
				self.bgImage.set_alpha(self.global_config['IMAGE_BG_ALPHA']['value'])
			except Exception,e:
				if DEBUG:print e
				self.bgImage=None

		#MAKE THE GAMEBOARD:
		visible=1
		spot_surface=self.create_default_spot_surface(visible)
		self.board=Board(
			self.global_config['M']['value'],
			self.global_config['N']['value'],
			self.global_config['WIN_W']['value']/2,
			self.global_config['WIN_H']['value']/2,
			None,
			spot_surface
		)
		self.boardspots=pygame.sprite.RenderPlain(self.board.get_spots())

		###
		#BUTTONS
		#reveal w.r.t. WIN_W
		reveal=20
		H0=self.global_config['WIN_H']['value']/2#-self.board.YBOT
		
		#ADMINBUTTONS
		self.admin_button=Button(self.global_config,'Admin',self.bfont)
		self.admin_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']-self.admin_button.get_width()/2-reveal,
			H0#self.global_config['WIN_H']['value']-self.admin_button.get_height()/2-H0
		)
		self.adminbuttongroup=pygame.sprite.Group()#[self.admin_button]
		self.adminbuttons=pygame.sprite.RenderPlain(self.adminbuttongroup)
		
		#PLAYBUTTONS
		self.demo_button=Button(self.global_config,'Demo',self.bfont)
		self.demo_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']-self.demo_button.get_width()/2-reveal,
			H0+1.2*self.demo_button.get_height()#self.global_config['WIN_H']['value']-5*self.demo_button.get_height()/2-2*reveal-H0
		)
		self.demobuttongroup=pygame.sprite.Group()#[self.demo_button]
		self.demobuttons=pygame.sprite.RenderPlain(self.demobuttongroup)
		
		self.play_button=Button(self.global_config,'Play',self.bfont)
		self.play_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']-self.play_button.get_width()/2-reveal,
			H0+2.4*self.play_button.get_height()#self.global_config['WIN_H']['value']-3*self.play_button.get_height()/2-reveal-H0
		)

		self.quit_button=Button(self.global_config,'Quit',self.bfont)
		self.quit_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']-self.quit_button.get_width()/2-reveal,
			H0+3.6*self.play_button.get_height()#self.global_config['WIN_H']['value']-3*self.play_button.get_height()/2-reveal-H0
		)

		self.playbuttongroup=pygame.sprite.Group([self.quit_button,self.demo_button,self.play_button,self.admin_button])
		self.playbuttons=pygame.sprite.RenderPlain(self.playbuttongroup)
		
		self.okay_button=RoundButton(self.global_config,'Okay',self.bfont)
		self.okay_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']-self.okay_button.get_width()/2-reveal,
			self.global_config['WIN_H']['value']-self.okay_button.get_width()/2-reveal#/2#-3*self.okay_button.get_height()/2-H0
		)
		self.quitbuttongroup=pygame.sprite.Group([self.okay_button])
		self.quitbuttons=pygame.sprite.RenderPlain(self.quitbuttongroup)


	def load_resources(self):	

		self.screen.fill((0,0,0))
		self.show_loading()
		
		t0=time.time()
		if DEBUG:print 'update_global_config_dependents 01:',"%3.3f"%(time.time()-t0)
		if DEBUG:print 'update_global_config_dependents 02:',"%3.3f"%(time.time()-t0)
		if DEBUG:print 'update_global_config_dependents 03:',"%3.3f"%(time.time()-t0)
		if DEBUG:print 'update_global_config_dependents 04:',"%3.3f"%(time.time()-t0)
		if DEBUG:print 'update_global_config_dependents 05:',"%3.3f"%(time.time()-t0)
		if DEBUG:print 'update_global_config_dependents 06:',"%3.3f"%(time.time()-t0)

		NTRAYSPOTS=7
		NNUMBERS=7
		
		self.NTRAYSPOTS=NTRAYSPOTS
		self.NNUMBERS=NNUMBERS
		
		trays=[]
		visible=1
		tray_spot_surface=self.create_default_spot_surface(visible)
		trays.append(	Board(1,NTRAYSPOTS,int(self.global_config['WIN_W']['value']/2.),self.board.YTOP/2,None,tray_spot_surface)	)#os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Images','new_spot.gif')
		trays.append(	Board(1,NTRAYSPOTS,int(self.global_config['WIN_W']['value']/2.),self.global_config['WIN_H']['value']-(self.global_config['WIN_H']['value']-self.board.YBOT)/2,None,tray_spot_surface)  )#os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Images','new_spot.gif')


		###
		visible=0
		submission_spot_surface=self.create_default_spot_surface(visible)
		self.submission=Board(
			self.global_config['M']['value'],
			self.global_config['N']['value'],
			self.global_config['WIN_W']['value']/2,
			self.global_config['WIN_H']['value']/2,
			None,
			submission_spot_surface
		)
		
		self.submissionspots=pygame.sprite.RenderPlain()
		
		if DEBUG:print 'update_global_config_dependents 07:',"%3.3f"%(time.time()-t0)
		
		#SETUP PLAYERS:
		
		self.players=[]#players have name,actor and solver
		self.tray_spots=[]
		self.target=pygame.sprite.RenderClear()#drag-n-drop object
		self.animation_in_progress=1
		
		player_names=[
			self.global_config['PLAYER_0_CHARACTER']['value'],
			self.global_config['PLAYER_1_CHARACTER']['value']
		]
		player_homes=[
			(self.global_config['WIN_W']['value']-100,100,0),
			(self.global_config['WIN_W']['value']-100,self.global_config['WIN_H']['value']-75,0)
		]
		for pidx in range(len(player_names)):
			indir=os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Actors',player_names[pidx])
			specific_maneuver_key=None
			rotozoom_tilesize=0
			actr=Actor(indir,self.global_config,player_homes[pidx][0],player_homes[pidx][1],player_homes[pidx][2],specific_maneuver_key,rotozoom_tilesize,images)
			self.players.append(Player(player_names[pidx],trays[pidx],actr,self))
			self.tray_spots.append(pygame.sprite.RenderPlain(self.players[pidx].tray.get_spots()))
		
		if DEBUG:print 'update_global_config_dependents 08.0:',"%3.3f"%(time.time()-t0)
		
		#DEFAULT PLAYER MODE IS ZERO:
		self.players[0].actor.queue('welcome')
		self.players[1].actor.queue('welcome')
		if self.MODE==1 and self.global_config['HUMAN_PLAYER_ZERO']['value']==1:
			self.players[0].set_mode(1)
		if self.MODE==1:
			self.players[1].set_mode(1)
		
		self.players[1].actor.queue('get_up')
		
		if DEBUG:print 'update_global_config_dependents 08.1:',"%3.3f"%(time.time()-t0)
		
		###
		self.AnimatedTiles=[]
		tiledir=os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Tiles')
		for m in range(self.global_config['M']['value']):
			row=[]
			for n in range(self.global_config['N']['value']):
				xc=self.board.get_spotMN(m,n).rect.center[0]
				yc=self.board.get_spotMN(m,n).rect.center[1]
				z=0
				specific_maneuver_key=None
				rotozoom_tilesize=1
				tile=Actor(tiledir,self.global_config,xc,yc,z,specific_maneuver_key,rotozoom_tilesize,images)
				row.append(tile)
				#tile.queue('hula')
			self.AnimatedTiles.append(row)
		if DEBUG:print 'update_global_config_dependents 08.2:',"%3.3f"%(time.time()-t0)
		
		
		
		if DEBUG:print 'update_global_config_dependents 09:',"%3.3f"%(time.time()-t0)


		#Try to load sounds:
		try:
			self.pickup_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','pickup01.wav')),]
			self.release_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','release01.wav')),]
			self.lockin_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','lockin01.wav')),]
			self.bounce_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','bounce01.wav')),]
			self.lose_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','lose01.wav')),]
			self.win_sounds		=[
									pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','win01.wav')),
									pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','win02.wav')),
									pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','win03.wav')),
						 		 ]
		except Exception,e:
			self.global_config['SOUNDON']['value']=0

		if self.global_config['DISPLAY_HIGH_SCORES']['value']==1:
			if len(self.global_config['HIGH_SCORES'])>0:
				highscore_string="High Score: %s %d"%(self.global_config['HIGH_SCORES'][0][0],self.global_config['HIGH_SCORES'][0][1])
				self.highscore_surface=self.hudfont.render(highscore_string,1,self.global_config['COLOR_HIGH_SCORES']['value'],self.global_config['COLOR_BG']['value'])
				self.highscore_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
		
		if DEBUG:print 'update_global_config_dependents 10:',"%3.3f"%(time.time()-t0)
		
		###########################
		
		###
		self.validator=TWS_Validator(self.board,self)
		if DEBUG:print 'update_global_config_dependents 08.3:',"%3.3f"%(time.time()-t0)
		self.localizer=TWS_Localizer(self.board,self)

		#TWS resource loading:
		keys=self.get_installed()#@twssolver.py
		
		if DEBUG:print keys
		#self.current_resource_key=keys[0]
		self.current_resource_key=self.global_config['DICTIONARY_RESOURCE']['value']
		self.load_resource()
		
		#Load special font if English-Chinese mode:
		if self.current_resource_key=='English-Chinese':
			self.overlayfont=pygame.font.Font(
				os.path.join(self.env.configdir,'Font',self.global_config['FONT_CHINESE']['value']),self.global_config['FONTSIZE_CHINESE']['value']
				#26#12
			)
			
		
		self.last_str_defn='Definition Area\n(click to clear)'
		self.set_last_defn(self.last_str_defn)

		#self.set_current_resource(self.current_resource)
		msg="%s (%d words)"%(self.current_resource_key,len(self.ntuple.keys()))
		self.set_current_resource(msg)
		
		if DEBUG:print 'update_global_config_dependents 11:',"%3.3f"%(time.time()-t0)
		
		
	def flip(self):
		pygame.display.flip()

	def load_config(self):
		
		if DEBUG:print 'tws.load_config'
		
		configdir	=self.env.configdir
		if DEBUG:print configdir,intermediate_path,fname
		homedir=os.getenv('HOME')
		if not homedir:homedir=os.getenv('USERPROFILE')
		infname=os.path.join(homedir,'.tws_config')
		
		if not os.path.exists(infname):
			master_fname=os.path.join(self.env.fontdir,'.tws_config_master')
			candidate=os.path.join('/','usr','share','games','tuxwordsmith','.tws_config_master')
			if os.path.exists(candidate):
				master_fname=candidate
				
			if self.env.OS=='win':
				cmd="copy %s %s"%(master_fname,os.path.join(homedir,'.tws_config'))
				os.system(cmd)
			else:
				cmd="cp %s %s"%(master_fname,os.path.join(homedir,'.tws_config'))
				os.system(cmd)
			
		inf=open(infname)
		content=inf.read()
		
		content=string.strip(content)
		
		config=eval(content)
		inf.close()

		resources=os.listdir(os.path.join(configdir,'xdxf'))
		for idx in range(len(resources)-1,-1,-1):
			if resources[idx][0]=='.':resources.remove(resources[idx])
		if DEBUG:print resources
		config['DICTIONARY_RESOURCE']['default']=resources
		if config['DICTIONARY_RESOURCE']['value']=='':config['DICTIONARY_RESOURCE']['value']=resources[0]

		return config

	def reload_configs(self):

		if DEBUG:print 'reload_configs:',self.player_idx,self.players[self.player_idx].mode,self.MODE
		self.global_config=self.load_config()

		resources=os.listdir(os.path.join(configdir,'xdxf'))
		for idx in range(len(resources)-1,-1,-1):
			if resources[idx][0]=='.':resources.remove(resources[idx])
		if DEBUG:print resources
		self.global_config['DICTIONARY_RESOURCE']['default']=resources
		#self.global_config['DICTIONARY_RESOURCE']['value']=resources[0]
		
		
	def show_letter_overlay(self,spot):
		
		tile=spot.guest
		uchar=tile.uchar
		#uname=uchar
		#cap_uchar=unicodedata.lookup(string.replace(uname,'SMALL','CAPITAL'))
		#uname=None
		uname=unicodedata.name(uchar)
		
		#commented out (12/28/07) try to make long multi-word char desc
		#try:
		#	small_uchar=unicodedata.lookup(string.replace(uname,'CAPITAL','SMALL'))
		#	uname=small_uchar
		#except:pass	
		
		ptval=tile.ptval
		#ncopy=self.global_config['distribution'][uname]
		
		msg=[]
		msg.append(uchar)
		if uname:msg.append(uname)
		msg.append("Value:%d"%(ptval))
		#msg.append("NCopy:%d"%(ncopy))
		
		self.display_overlay(self.overlayfont_small,msg)
		

	def show_dist_overlay(self):
		if DEBUG:print 'show_dist_overlay'
		#return
		
		#make this pretty formatted table overlay with levels/ranges/scores broken-up into square regions in 2D
		
		msg=[]
		
		msg.append("Charset has %d unique characters"%(len(self.global_config['distribution'].keys())))
		ctot=0
		for uname in self.global_config['distribution'].keys():ctot+=self.global_config['distribution'][uname]
		msg.append("Total setsize is %d characters"%(ctot))
		msg.append(u' ')
		
		sorted_keys=self.global_config['distribution'].keys()
		sorted_keys.sort()
		for idx in range(len(sorted_keys)):
			try:
				uname=sorted_keys[idx]
				cap_uchar=unicodedata.lookup(string.replace(uname,'SMALL','CAPITAL'))
				small_uchar=unicodedata.lookup(string.replace(uname,'CAPITAL','SMALL'))
				line="%3s %3s %3d %3d %s"%(cap_uchar,small_uchar,self.global_config['distribution'][uname],self.global_config['scoring'][uname],uname)
				msg.append(line)
			except Exception,e:
				print sorted_keys[idx]
				print e
				if DEBUG:print e
				
		self.display_overlay(self.overlayfont_small,msg)

	def go_help(self):
		self.screen.fill((0,0,0))
		self.show_help()		
		self.flip()
		while 1:
			breakout=0
			for event in pygame.event.get([KEYUP]):
				if event.type == KEYUP:breakout=1
				self.KDOWN=0
				self.TDOWN=0
			if breakout:break
		
	def focus_definition(self):
		self.screen.fill(self.global_config['COLOR_BG']['value'])

		self.screen.blit(self.bkg,(0,0))
		if self.bgImage:
			self.screen.blit(self.bgImage,(0,0))

		self.screen.blit(self.last_defn_surface,(20,self.y00))
		self.flip()
		
		while 1:
			breakout=0
			for event in pygame.event.get([KEYUP]):
				if event.type == KEYUP:breakout=1
				self.KDOWN=0
				self.TDOWN=0
			if breakout:break
	
		
	def show_help(self):
		
		self.screen.fill(self.global_config['COLOR_BG_HUD']['value'])
		linesize=self.hudfont.size('------------------------------------------------------------------------')
		
		msgs=[
			u'------------------------------------------------------------------------',
			u'                                   HELP                                 ',
			u'------------------------------------------------------------------------',
			u'                                                                        ',
			u'F1  Key: Clear definition area                                          ',
			u'F2  Key: Fill background and show definition only (to help read)        ',
			u'F3  Key: Record movie (screenshot ea. frame)                            ',
			u'F4  Key: Screensaver mode                                               ',
			u'F5  Key: Shuffle tiles in place                                         ',
			u'F7  Key: Throw back moved tiles to tray                                 ',
			u'F8  Key: Skip turn and exchange all tiles                               ',
			u'F9  Key: Show help                                                      ',
			u'F10 Key: Show credits                                                   ',
			u'F11 Key: Screenshot to HOME directory                                   ',
			u'F12 Key: Fullscreen (Linux only)                                        ',
			u'ESC Key: Exit                                                           ',
			u'                                                                        ',
			u'Mouse wheel also shuffles tiles in place                                ',
			u'Left-click background to clear definition area                          ',
			u'Left-click on word shows definition/translation overlay                 ',
			u'Right-click on letter shows character info overlay                      ',
			u'Right-click on background shows character distribution                  ',
			u'                                                                        ',
			u'Changing languages: Admin->DICTIONARY_RESOURCE                          ',
			u'Background Images: Admin-> IMAGE_BG                                     ',
			u'Hide bad animations: Admin->PLAYER_0_CHARACTER->None                    ',			
			u'Turning on sound: Admin->SOUNDON->true                                  ',
		]
		
		y0=self.global_config['WIN_H']['value']/2-len(msgs)/2.*linesize[1]
		fg_hud=None
		bg_hud=None
		
		for msg_idx in range(len(msgs)):
			
			if msg_idx==1:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_HILIGHT']['value']
			else:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_SPOT']['value']
			
			bg_hud=self.global_config['COLOR_BG_HUD']['value']
			help_surface=font.render(
				msgs[msg_idx],1,
				fg_hud,
				bg_hud 
			)	
			hs_w=linesize[0]
			hs_h=help_surface.get_size()[1]
			self.screen.blit(help_surface,(self.global_config['WIN_W']['value']/2.-hs_w/2.,y0+msg_idx*linesize[1]))
			

	def show_credit(self):
		
		self.screen.fill(self.global_config['COLOR_BG_HUD']['value'])
		linesize=self.hudfont.size('text to determine font size')
		
		msgs=[
			u'This software was written for',
			u'Millie and Jordan',
			u'* And * Kids * Everywhere *',
			u'',
			u'TuxWordSmith Version 0.8.0',
			u'December 6, 2014',
			u'',
			u'Author:Charles B. Coss'+u'\xe9',
			u'Contact:ccosse@asymptopia.org', 
			u'Website: www.asymptopia.org',
		]
		
		y0=self.global_config['WIN_H']['value']/2-len(msgs)/2.*linesize[1]
		fg_hud=None
		bg_hud=None
		
		for msg_idx in range(len(msgs)):
			
			if msg_idx==1:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_HILIGHT']['value']
			else:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_SPOT']['value']
			
			bg_hud=self.global_config['COLOR_BG_HUD']['value']
			credit_surface=font.render(
				msgs[msg_idx],1,
				fg_hud,
				bg_hud 
			)	
			cs_w=credit_surface.get_size()[0]
			cs_h=credit_surface.get_size()[1]
			self.screen.blit(credit_surface,(self.global_config['WIN_W']['value']/2.-cs_w/2.,y0+msg_idx*linesize[1]))
	
	def show_loading(self):
		
		linesize=self.hudfont.size('text to determine font size')
		y0=self.global_config['WIN_H']['value']/2-1/2.*linesize[1]
		fg_hud=self.global_config['COLOR_FG']['value']
		bg_hud=self.global_config['COLOR_BG_HUD']['value']
		font=self.hudfont
		credit_surface=font.render(
			u'... Loading ...',
			1,
			fg_hud,
			bg_hud
		)
		
		cs_w=credit_surface.get_size()[0]
		cs_h=credit_surface.get_size()[1]
		self.screen.fill(self.global_config['COLOR_BG_HUD']['value'])
		self.screen.blit(credit_surface,(self.global_config['WIN_W']['value']/2.-cs_w/2.,y0+linesize[1]))
		pygame.display.flip()
		
		
	
	def go_credit(self):		
		self.screen.fill(self.global_config['COLOR_BG_HUD']['value'])
		self.show_credit()		
		self.flip()
		while 1:
			breakout=0
			for event in pygame.event.get([KEYUP]):
				if event.type == KEYUP:breakout=1
				self.KDOWN=0
				self.TDOWN=0
			if breakout:break
		
	def go_screenshot(self):
		display_surface=pygame.display.get_surface()
		tstamp=self.mktstamp()
		oufname="TuxWordSmith_%s.bmp"%(tstamp)
		try:
			oufname=os.path.join(os.environ['HOME'],oufname)
		except Exception,e:
			if DEBUG:print `e`
		
		pygame.image.save(display_surface,oufname)
		return 1

	def go_fullscreen(self):
		self.AMFULLSCREEN=pygame.display.toggle_fullscreen()
		if DEBUG:print 'self.AMFULLSCREEN=',self.AMFULLSCREEN

	def display_overlay(self,xfont,msg):#msg=[line1,line2,...]
		wmax=0
		hmax=0
		htot=0
		for idx in range(len(msg)):
			linesize=xfont.size(msg[idx]+'m')
			lineW=linesize[0]
			lineH=linesize[1]
			if lineW>wmax:wmax=lineW
			if lineH>hmax:hmax=lineH
			htot+=hmax
			
		overlay_surface=pygame.Surface((wmax+40,htot+2*hmax))
		overlay_surface.fill(self.global_config['COLOR_BG_OVERLAY']['value'])
		for idx in range(len(msg)):
			font_surface=xfont.render(msg[idx],1,self.global_config['COLOR_FG_OVERLAY']['value'],self.global_config['COLOR_BG_OVERLAY']['value'])	
			overlay_surface.blit(
				font_surface,
				(20,(idx+1)*hmax)
			)
		overlay_surface.set_alpha(self.global_config['COLOR_BG_OVERLAY_ALPHA']['value'])
		
		#work-out tlc_xy to center the overlay:
		tlcx=self.global_config['WIN_W']['value']/2-overlay_surface.get_width()/2
		tlcy=self.global_config['WIN_H']['value']/2-overlay_surface.get_height()/2
		#font_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
		self.screen.blit(overlay_surface,(tlcx,tlcy))#spot.rect[0],spot.rect[1]
		self.flip()
		
		while 1:
			breakout=0
			for event in pygame.event.get():
				if event.type == KEYDOWN:breakout=1
				elif event.type == MOUSEBUTTONDOWN:breakout=1
			if breakout:break
			
		self.update()#to ensure popdown before next overlay

	def progress_message(self,msg):
		self.screen.fill(self.global_config['COLOR_BG_HUD']['value'])
		linesize=self.hudfont.size(msg)
		y0=self.global_config['WIN_H']['value']/2-1/2.*linesize[1]
		fg_hud=self.global_config['COLOR_FG']['value']
		bg_hud=self.global_config['COLOR_BG_HUD']['value']
		font=self.hudfont
		credit_surface=font.render(
			msg,
			1,
			fg_hud,
			bg_hud
		)
		
		cs_w=credit_surface.get_size()[0]
		cs_h=credit_surface.get_size()[1]
		self.screen.blit(credit_surface,(self.global_config['WIN_W']['value']/2.-cs_w/2.,y0+linesize[1]))
		pygame.display.flip()
	
	def make_feedback_table_cell(self,w,h,frame_color,msg):
		frame_surf=pygame.Surface((w,h), flags=0, depth=0, masks=None)
		frame_surf.fill(frame_color)
		inset_surf=pygame.Surface((frame_surf.get_width()-2,frame_surf.get_height()-2))
		inset_surf.fill(self.global_config['COLOR_BG']['value'])
		frame_surf.blit(inset_surf,(1,1))
		score_surf=self.hudfont.render(msg,1,frame_color,self.global_config['COLOR_BG']['value'])
		tlcxy=(frame_surf.get_width()/2-score_surf.get_width()/2,frame_surf.get_height()/2-score_surf.get_height()/2)
		frame_surf.blit(score_surf,tlcxy)
		frame_surf.set_colorkey(self.global_config['COLOR_BG']['value'])
		return frame_surf

	def draw_feedback_overlay(self):
		
		button_width=80
		button_height=30
		frame_color=self.global_config['COLOR_FG']['value']
		yc_player_0_tray=self.players[0].tray.YTOP+(self.players[0].tray.YBOT-self.players[0].tray.YTOP)/2
		yc_player_1_tray=self.players[1].tray.YTOP+(self.players[1].tray.YBOT-self.players[1].tray.YTOP)/2
		
		###players[0].score
		score_string="Score:%3d"%(self.players[0].score)
		frame_surf=self.make_feedback_table_cell(button_width,button_height,frame_color,score_string)
		self.screen.blit(frame_surf,((self.board.XLHS-button_width)/2,yc_player_0_tray-button_height/2))#self.board.YTOP
		
		###players[1].score
		score_string="Score:%3d"%(self.players[1].score)
		frame_surf=self.make_feedback_table_cell(button_width,button_height,frame_color,score_string)
		self.screen.blit(frame_surf,((self.board.XLHS-button_width)/2,yc_player_1_tray-button_height/2))#self.board.YBOT-button_height
		
		###level indicator
		level_string="Level: %d"%(self.LEVEL)
		frame_surf=self.make_feedback_table_cell(button_width,button_height,frame_color,level_string)
		self.screen.blit(frame_surf,((self.board.XLHS-button_width)/2,self.global_config['WIN_H']['value']/2-button_height/2))#self.board.YBOT-button_height
		
		if DEBUG:
			#draw crosshairs
			pygame.draw.line(self.screen, frame_color, (self.global_config['WIN_W']['value']/2,0), (self.global_config['WIN_W']['value']/2,self.global_config['WIN_H']['value']), 1)
			pygame.draw.line(self.screen, frame_color, (0,self.global_config['WIN_H']['value']/2), (self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']/2), 1)
			
			pygame.draw.line(self.screen, frame_color, (0,yc_player_0_tray), (self.global_config['WIN_W']['value'],yc_player_0_tray), 1)

			pygame.draw.line(self.screen, frame_color, (0,yc_player_1_tray), (self.global_config['WIN_W']['value'],yc_player_1_tray), 1)

			startpos=(self.board.XLHS/2,self.board.YTOP)
			endpos=(self.board.XLHS/2,self.board.YBOT)
			pygame.draw.line(self.screen, frame_color, startpos, endpos, 1)

	def queue_thinking_maneuver(self):
		self.players[self.player_idx].actor.queue('thinking')
		self.update()
		
		#WHY?: this keeps players from moving before he arrives at lhs; 
		while self.animation_in_progress:
			self.update()
			if self.STOP_RUNNING:break

	def update_highscores(self):
		if DEBUG:print 'update_highscores',self.global_config['DISPLAY_HIGH_SCORES']['value']
		if not self.global_config['DISPLAY_HIGH_SCORES']['value']:return
		
		for idx in range(len(self.players)):
			if self.players[idx].mode==1:
				
				flag=0
				score=self.players[idx].score
				initials=self.get_user_initials(idx)
				for insert_idx in range(len(self.global_config['HIGH_SCORES'])):
					if score>self.global_config['HIGH_SCORES'][insert_idx][1]:
						self.global_config['HIGH_SCORES'].insert(insert_idx,(initials,score))
						flag=1
						break
				
				if not flag:self.global_config['HIGH_SCORES'].append((initials,score))
				
		while len(self.global_config['HIGH_SCORES'])>self.global_config['NUM_HIGH_SCORES_TO_KEEP']:
			self.global_config['HIGH_SCORES'].pop()
		
		if DEBUG:print 'calling admin.update_highscores()'
		self.admin.update_highscores()
		
	def get_user_initials(self,idx):
		
		letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
		
		#idx0=int(random()*len(letters))
		#idx1=int(random()*len(letters))
		#idx2=int(random()*len(letters))
		#rval="%c%c%c"%(letters[idx0],letters[idx1],letters[idx2])
		
		have3x=0
		submission=''
		submission_size=self.appnamefont.size('Initials: ')
		x_lhs=self.global_config['WIN_W']['value']/2-submission_size[0]
		y_top=self.global_config['WIN_H']['value']/2-submission_size[1]/2
		
		while not have3x:
			
			for event in pygame.event.get():
				
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					if len(submission)==0:return '???'
					return submission
				
				if event.type == KEYDOWN:
					
					t0=time.mktime(time.localtime())
					
					if pygame.key.name(event.key)=='return':
						have3x=1
					
					elif pygame.key.name(event.key)==('backspace'):
						if len(submission)>0:submission=submission[:-1]
						
					else:
						try:
							newchar=string.upper(pygame.key.name(event.key))
							dummy=letters.index(newchar)
							if len(submission)<3:submission=submission+newchar
						except:pass
			
			if self.bgImage:self.screen.blit(self.bgImage,(0,0))
			else:self.screen.blit(self.bkg,(0,0))
			
			who="Enter Player %d Initials"%(idx)
			who_surface=self.appnamefont.render(who,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value'])
			who_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
			self.screen.blit(who_surface,(self.global_config['WIN_W']['value']/2-who_surface.get_width()/2,self.global_config['WIN_H']['value']/3))
			
			submission_surface=self.appnamefont.render('Initials: '+submission,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value'])
			submission_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
			submission_size=self.appnamefont.size('Initials: '+submission)
			self.screen.blit(submission_surface,(x_lhs,y_top))
			self.flip()
			
		if len(submission)==0:return '???'
		return submission

	def on_exit(self):
		lines=[
			'',
			'**********************************************************',
			'*                                                        *',
			'*   You are using version 0.8.0 from December 6, 2014   *',
			'*                                                        *',
			'*                http://www.asymptopia.org               *',
			'*                                                        *',
			'*         AsymptopiaSoftware | Software@theLimit         *',
			'*                                                        *',
			'**********************************************************',
			'',
		]
		
		for line in lines:print line
		pygame.quit()
		sys.exit()

	def set_last_defn(self,str_defn):#this always takes a string #changing to accept unicode now..from solver
		lines=[]
		split_defn=string.split(str_defn,'\n')
		max_idx=max(1,len(split_defn))
		
		
		#further split ultra-long lines > nc:
		split_idx=0
		while 1:
			if split_idx >= len(split_defn):break
			
			line=split_defn[split_idx]
			tmp_linesize=self.overlayfont.size(line+'m')
			
			if tmp_linesize[0]>self.global_config['WIN_W']['value']-30:
				
				split_line=string.split(line,' ',1000)
				aux_split_line=[]
				aux_line=''
				
				while tmp_linesize[0]>self.global_config['WIN_W']['value']-30:
					
					aux_split_line.insert(0,split_line.pop())
					
					line=''
					for lidx in range(len(split_line)):
						line="%s%s "%(line,split_line[lidx])
					
					aux_line=''
					for lidx in range(len(aux_split_line)):
						aux_line="%s%s "%(aux_line,aux_split_line[lidx])
						
					tmp_linesize=self.overlayfont.size(line+'m')
					
				split_defn[split_idx]=line
				split_defn.insert(split_idx+1,aux_line)
			
			split_idx+=1
					
		
		linesize=None
		wmax=0
		hmax=0
		for idx in range(max_idx):
			tmp_linesize=self.overlayfont.size(split_defn[idx]+'m')
			if tmp_linesize[0]>wmax:
				wmax=tmp_linesize[0]
				linesize=tmp_linesize
		
		x0=0
		y0=0
		
		if DEBUG:print 'setting self.last_defn_surface:',linesize
		self.last_defn_surface=pygame.Surface((linesize[0],(max_idx+1)*linesize[1]))
		self.last_defn_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
		
		fg_hud=self.global_config['COLOR_FG']['value']
		bg_hud=self.global_config['COLOR_BG']['value']
		self.last_defn_surface.fill(bg_hud)
		
		bidx=0
		
		if DEBUG:print split_defn
		
		for idx in range(len(split_defn)):
			if split_defn[idx]=='':continue
			
			if DEBUG:
				try:print idx,split_defn[idx]
				except Exception,e:print e
			
			if string.find(split_defn[idx],'[')>-1:
				try:
					split_defn[idx]=eval(split_defn[idx])
					tmp=u''
					for vidx in range(len(split_defn[idx])):
						tmp="%s %s"%(tmp,split_defn[idx][vidx])
					split_defn[idx]=tmp
				except:
					pass
					
			surf=self.overlayfont.render(
				   split_defn[idx],1,
				   fg_hud,#self.global_config['fgcolor'],
				   bg_hud #self.global_config['bgcolor']
			)
			self.last_defn_surface.blit(
				surf,
				(x0,y0+bidx*linesize[1])
			)
			bidx+=1
		
		#self.last_defn=split_defn
		#if DEBUG:print 'self.last_defn:',self.last_defn


	def validate(self,submission):
		
		exprtype=None
		
		letters=self.global_config['letters']
		idx_map=self.board.get_idx_map(letters)#idx_map does return 2D array of uchars
		
		#put into rlist form
		rlist=[]
		
		if DEBUG:print submission
		
		for spot in submission:
			m=spot.M
			n=spot.N
			
			try:
				str_val=spot.guest.str_val
				uchar=spot.guest.uchar
			except Exception,e:
				continue
						
			#letter=self.get_unidesc_field(uchar,'VALUE')
			#mod=self.get_unidesc_field(uchar,'MOD')
			#if not mod:mod='NOMOD'
			#gc_scoring_key="%s_%s"%(letter,mod)
			
			rlist.append([uchar,m,n])	
			#rlist.append((str_val,m,n))
			
		#sort the rlist on fields 1&2
		rlist=self.sort_on_field(rlist,1)
		rlist=self.sort_on_field(rlist,2)
		if DEBUG:print 'rlist=',rlist
		
		
		#determine row or col:
		if len(rlist)>1:
			if rlist[0][1]==rlist[1][1]:exprtype='row'
			elif rlist[0][2]==rlist[1][2]:exprtype='col'
		elif len(rlist)==1:
			#check 4 directions
			m=rlist[0][1]
			n=rlist[0][2]
			if m>0:
				if idx_map[m-1][n]!='--':exprtype='col'
			if m<self.global_config['M']['value']-1:
				if idx_map[m+1][n]!='--':exprtype='col'
			if n>0:
				if idx_map[m][n-1]!='--':exprtype='row'
			if n<self.global_config['N']['value']-1:
				if idx_map[m][n+1]!='--':exprtype='row'
			
			
		else:return False
		
		#check ends and existing tiles:
		#check for L-R continuity
		if exprtype=='row':
			#if rlist[0][1]>0:
			
			if DEBUG:print 'checking left'
			for idx in range(rlist[0][2]-1,-1,-1):
				m=rlist[0][1]
				n=idx
				if idx_map[m][n]!='--':
					str_val=letters[eval(idx_map[m][n])]
					if DEBUG:print 'prepending ',str_val
					rlist.insert(0,(str_val,m,n))
				else:break
						
			if DEBUG:print 'checking right'
			#if rlist[len(rlist)-1][2]<self.global_config['N']-1:
			for idx in range(rlist[len(rlist)-1][2]+1,self.global_config['N']['value']):
				m=rlist[0][1]
				n=idx
				if idx_map[m][n]!='--':
					str_val=letters[eval(idx_map[m][n])]
					if DEBUG:print 'appending ',str_val
					rlist.append((str_val,m,n))
				else:
					if DEBUG:print 'nothing:',m,n,idx_map[m][n]
					break
					
			if DEBUG:print 'checking between'
			for idx in range(len(rlist)):
				if rlist[idx][2]!=rlist[0][2]+idx:
					map_m=rlist[0][1]
					map_n=rlist[0][2]+idx
					if idx_map[map_m][map_n]!='--':
						str_val=letters[eval(idx_map[map_m][map_n])]
						if DEBUG:print 'inserting ',str_val
						entry=(str_val,map_m,map_n)
						rlist.insert(idx,entry)
					else:return False
				
				else:#check above/below
					#above
					map_m=rlist[0][1]-1
					map_n=rlist[0][2]+idx
					if map_m>0:
						if idx_map[map_m][map_n]!='--':
							if idx_map[map_m+1][map_n]!='--':continue#i.e existing
							if DEBUG:print '661:',idx_map[map_m][map_n]
							return False
					
					#below
					map_m=rlist[0][1]+1
					map_n=rlist[0][2]+idx
					if map_m<self.global_config['M']['value']:
						if idx_map[map_m][map_n]!='--':
							if idx_map[map_m-1][map_n]!='--':continue#i.e existing
							if DEBUG:print '670:',idx_map[map_m][map_n]
							return False
					
					
		if exprtype=='col':
			
			#if rlist[0][1]>0:
			if DEBUG:print 'checking above'
			for idx in range(rlist[0][1]-1,-1,-1):
				m=idx
				n=rlist[0][2]
				if idx_map[m][n]!='--':
					str_val=letters[eval(idx_map[m][n])]
					if DEBUG:print 'prepending ',str_val
					rlist.insert(0,(str_val,m,n))
				else:
					break
						
			if DEBUG:print 'checking below'
			#if rlist[len(rlist)-1][1]<self.global_config['M']-1:
			for idx in range(rlist[len(rlist)-1][1]+1,self.global_config['M']['value']):
				m=idx
				n=rlist[0][2]
				if idx_map[m][n]!='--':
					str_val=letters[eval(idx_map[m][n])]
					if DEBUG:print 'appending ',str_val
					rlist.append((str_val,m,n))
				else:
					break
			
			if DEBUG:print 'checking between'		
			for idx in range(len(rlist)):
				if rlist[idx][1]!=rlist[0][1]+idx:
					map_m=rlist[0][1]+idx
					map_n=rlist[0][2]
					if idx_map[map_m][map_n]!='--':
						str_val=letters[eval(idx_map[map_m][map_n])]
						if DEBUG:print 'inserting ',str_val
						entry=(str_val,map_m,map_n)
						rlist.insert(idx,entry)
					else:
						if DEBUG:print '709:',rlist[idx][1],rlist[0][1]+idx
						return False
					
				else:#check left/right
					#left
					map_m=rlist[0][1]+idx
					map_n=rlist[0][2]-1
					if map_n>0:
						if idx_map[map_m][map_n]!='--':
							if idx_map[map_m][map_n+1]!='--':continue#i.e existing
							if DEBUG:print '718:',idx_map[map_m][map_n]
							return False
					
					#right
					map_m=rlist[0][1]+idx
					map_n=rlist[0][2]+1
					if map_n<self.global_config['N']['value']:
						if idx_map[map_m][map_n]!='--':
							if idx_map[map_m][map_n-1]!='--':continue#i.e existing
							if DEBUG:print '726:',idx_map[map_m][map_n]
							return False
			
			
			
		
		#print fixed-up rlist
		if DEBUG:print 'rlist=',rlist
		
		#confirm is key in dict
		word=u''
		if DEBUG:print rlist
		for idx in range(len(rlist)):
			word+=rlist[idx][0]
			
		last_article=self.players[self.player_idx].solver.get_article(word)
		
		if last_article['key']!=None:	
			self.last_str_defn="%s: %s"%(word,last_article['content'])#(unicode(word).encode('UTF-8'),unicode(last_article['content']).encode('UTF-8'))
			if DEBUG:print self.last_str_defn
			self.set_last_defn(self.last_str_defn)
			fp_list=self.players[self.player_idx].solver.mkfingerprint(word)
			scrabble_sum=self.players[self.player_idx].solver.get_scrabble_sum(fp_list)
			self.players[self.player_idx].score+=scrabble_sum
			return True
		
		else:
			self.last_str_defn=word+": %s"%('Not Found In Resource')
			self.set_last_defn(self.last_str_defn)
			return False


	def sort_on_field(self,l,i):#l=2Dlist, i=idx of each row to sort on
		for idx0 in range(len(l)):
			for idx1 in range(idx0,len(l)):
				if l[idx1][i]<l[idx0][i]:
					tmp=l.pop(idx1)
					l.insert(idx0,tmp)
		
		return l

	def set_current_resource(self,current_resource):
		if DEBUG:print 'set_current_resource:',current_resource,type(current_resource)
		linesize=self.hudfont.size(current_resource)
		fg_hud=(255,255,255)
		bg_hud=self.global_config['COLOR_BG']['value']
		self.current_resource_surface=self.hudfont.render(
			current_resource,1,
			fg_hud,
			bg_hud 
		)	
		self.current_resource_surface.set_colorkey(self.global_config['COLOR_BG']['value'])

	def show_defn_overlay(self,spot):
		
		if DEBUG:
			try:print 'setting:',spot.msg
			except Exception,e:print e
		
		last_str_defn=spot.msg
		self.set_last_defn(last_str_defn)
		return
		
		#msg=spot.msg
		#if DEBUG:print `msg`
		#self.display_overlay(self.overlayfont_small,msg)

	def go_splash(self):
		
		self.ytop=self.global_config['WIN_H']['value']/2-20
		
		#here we just adjust ytop for possible highscore list below appname:
		dy=10#space btw appname and highscore list
		if self.global_config['DISPLAY_HIGH_SCORES']['value']==1:
			if len(self.global_config['HIGH_SCORES'])>0:
				highscore_string="High Score %02d: %s %d"%(0,self.global_config['HIGH_SCORES'][0][0],self.global_config['HIGH_SCORES'][0][1])
				test_surface=self.hudfont.render(highscore_string,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value'])
				surf_height=test_surface.get_height()
				self.ytop-=max(len(self.global_config['HIGH_SCORES'])*surf_height,0)
		
		self.screen.fill((0,0,0))
		fg_hud=self.global_config['COLOR_FG']['value']
		bg_hud=self.global_config['COLOR_BG']['value']
		#self.screen.fill(self.global_config['COLOR_BG']['value'])

		self.fwoverlay=FWOverlay(
			self.screen,
			self.global_config['FIREWORKS_DT']['value'],
			self.global_config['FIREWORKS_DT_LAUNCH']['value'],
			self.global_config['FIREWORKS_SCALEFACTOR']['value']
		)
		
		self.STOP_RUNNING=0
		
		self.helpstring="Help:F9"
		hsurf=self.hudfont.render(self.helpstring,1,(255,255,255),(0,0,0))
		hsurf.set_colorkey((0,0,0))
		H0=self.global_config['WIN_H']['value']-50
		xhelp=self.global_config['WIN_W']['value']-self.admin_button.get_width()/2-45
		yhelp=self.global_config['WIN_H']['value']/2-40
		
		surf1=self.appnamefont.render('TuxWordSmith',1,self.global_config['COLOR_FG']['value'],(0,0,0))
		surf1_w=surf1.get_size()[0]
		surf1_h=surf1.get_size()[1]
		surf1.set_colorkey((0,0,0))
		
		surf2=self.overlayfont_small.render('AsymptopiaSoftware | Software@theLimit',1,self.global_config['COLOR_BG']['value'],(0,0,0))
		surf2_w=surf2.get_size()[0]
		surf2_h=surf2.get_size()[1]
		surf2.set_colorkey((0,0,0))
		
		surf3=self.overlayfont_small.render('www.asymptopia.org',1,self.global_config['COLOR_BG']['value'],(0,0,0))
		surf3_w=surf3.get_size()[0]
		surf3_h=surf3.get_size()[1]
		surf3.set_colorkey((0,0,0))
		
		count=0
		self.t_last=time.time()

		while True:
			
			if not len(self.fwoverlay.projectiles):
				if self.SCREENSAVER:
					self.fwoverlay.make_volley(self.global_config['FIREWORKS_SETSIZE']['value'])
				
			if self.STOP_RUNNING!=0:
				#self.onexit()
				#print 'returning ',self.MODE
				return(self.MODE,self.AMFULLSCREEN)
			
			if not self.global_config['SCREENSAVER_ON_AT_START']['value']:
				if time.time()-self.t_last<0.5:
					time.sleep(.1)
					continue
				self.t_last=time.time()

			breakout=self.handle_mouse()
			
			#self.handle_keyboard()
			for event in pygame.event.get(KEYDOWN):
				
				if event.key == K_ESCAPE:
					pygame.quit()
					self.on_exit()
					#sys.exit()
					#self.MODE-=1
					#self.STOP_RUNNING=1
					#return
				
				elif event.key==K_F9:
					self.go_help()
				
				elif event.key==K_F10:
					self.go_credit()
					
				elif event.key ==K_F12:
					pygame.display.toggle_fullscreen()
					self.AMFULLSCREEN*=-1
					
				elif event.key==K_F11:
					try:self.take_screenshot()
					except:pass
			
			pygame.event.clear()
			
			self.screen.fill((0,0,0))
			
			if self.SCREENSAVER:
				self.fwoverlay.tick()

			if self.MODE==0:
				self.demobuttons.draw(self.screen)
				self.playbuttons.draw(self.screen)
				self.adminbuttons.draw(self.screen)
				self.screen.blit(hsurf,(xhelp,yhelp))
				
			ytop=self.ytop
			self.screen.blit(surf1,(self.global_config['WIN_W']['value']/2.-surf1_w/2,ytop))
			ytop+=surf1_h
			self.screen.blit(surf2,(self.global_config['WIN_W']['value']/2.-surf2_w/2,ytop))
			ytop+=surf2_h
			self.screen.blit(surf3,(self.global_config['WIN_W']['value']/2.-surf3_w/2,ytop))
			ytop+=surf3_h
			
			
			pygame.display.flip()
			if breakout:break
