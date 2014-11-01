#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2010 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import wx
from wxadmin import *
from tws import *

class TuxWordSmithAppWX(wx.App):
	
	def __init__(self):
		wx.App.__init__(self, 0)
		
		mode=0#-1,0,1,2 = quit/screensaver/play/admin
		level=4
		use_default_level=True
		
		while True:
			
			prog=TuxWordSmith(mode,level,use_default_level,True)
			#rval=prog.admin.ShowModal()
			#sys.exit()
			mode,level=prog.run()
			
			
			if mode<0:prog.on_exit()
			elif mode==0:pass#prog.update_highscores()
			elif mode==1:prog.update_highscores()
			elif mode==2:
				rval=prog.admin.ShowModal()
				mode=0
			
			use_default_level=0
