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
import os,sys,string,time,types
from random import *
import wx

import  wx.lib.scrolledpanel as scrolled

from pygame import *

from cfgctrlobj import *
from dict_formatter import *

DEBUG=0

class CfgCtrl(wx.Panel):
	
	def __init__(self,parent,nb,tab_name):
		
		self.parent=parent
		self.nb=nb
		self.tab_name=tab_name
		self.env=self.parent.env
		self.global_config=self.parent.global_config
		
		self.cfg=None
		self.sizer=None
		self.cp=None
		self.cpbox=None
		self.cfgctrlobjs=[]
		self.SHOW_ALL=0
		
		self.ID=wx.NewId()
		wx.Panel.__init__(self,nb,self.ID,wx.DefaultPosition,wx.DefaultSize,style=wx.FULL_REPAINT_ON_RESIZE)#wxVSCROLL|
		
	def setup(self):
		button_height=30
		if self.env.OS=='win':button_height=20
		button_size=wx.Size(100,button_height)
		self.toolbar=wx.ToolBar(self,wx.NewId(),style=wx.TB_HORIZONTAL)# | wxNO_BORDER | wxTB_FLAT | wxTB_TEXT
		#self.toolbar.SetBackgroundColour(self.global_config['COLOR_BG_CFG']['value'])
		
		xpos=0
		if self.tab_name=='Globals':
			#...........................................................
			#SAVE BUTTON
			xid=wx.NewId()
			saveB=wx.Button(self.toolbar,xid,"Save",size=button_size,pos=wx.Point(xpos,0))
			self.toolbar.AddControl(saveB)
			saveB.SetToolTip(wx.ToolTip('Save these configuration options'))
			wx.EVT_BUTTON(self.toolbar,xid,self.saveCB)
			xpos+=100
	
			#...........................................................
			#LOGOUT BUTTON
			xid=wx.NewId()
			logoutB=wx.Button(self.toolbar,xid,"Hide",size=button_size,pos=wx.Point(xpos,0))
			logoutB.SetToolTip(wx.ToolTip('Hide the Administrator Control Panel.'))
			self.toolbar.AddControl(logoutB)
			wx.EVT_BUTTON(self.toolbar,xid,self.logoutCB)
			xpos+=100
			
			#...........................................................
			#SHOW_ALL TOGGLE
			xid=wx.NewId()
			showallB=wx.CheckBox(self.toolbar,xid,"ShowAll",size=button_size,pos=wx.Point(xpos,0))
			showallB.SetValue(self.SHOW_ALL)
			showallB.SetToolTip(wx.ToolTip('Show all configurable parameters, including those hidden by default'))
			self.toolbar.AddControl(showallB)
			wx.EVT_CHECKBOX(self.toolbar,xid,self.showallCB)
			
		self.cp=scrolled.ScrolledPanel(self,wx.NewId(),wx.DefaultPosition,style=wx.FULL_REPAINT_ON_RESIZE|wx.ALWAYS_SHOW_SB|wx.VSCROLL)
		self.cp.SetupScrolling()

		self.cp.SetBackgroundColour(self.global_config['COLOR_BG_ADMIN']['value'])
		
		self.sizer=wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.toolbar,0,wx.EXPAND)
		self.sizer.Add(self.cp,1,wx.GROW,1)
		self.SetSizer(self.sizer)
		self.SetAutoLayout(True)
		self.Layout()
		
		if self.tab_name=='Accounts':self.reload('new')
		elif self.tab_name=='Globals':self.reload('globals')
		elif self.tab_name=='Readme':self.reload('Readme')
		elif self.tab_name=='GPL':self.reload('GPL')
		elif self.tab_name=='Asymptopia':self.reload('Asymptopia')
		
	def deleteCB(self,e):
	
		if self.cfg['CFGNAME']=='new':return
		if self.cfg['CFGNAME']=='admin':return
		if self.cfg['CFGNAME']=='guest':return
		if self.cfg['CFGNAME']=='globals':return
		if self.cfg['CFGNAME']=='default':return
		
		fname=os.path.join(self.env.configdir,self.tab_name,self.cfg['CFGNAME'])
		try:os.removedirs(fname)
		except:pass#print 'unable to recursively delete 1x',fname
		
		cmd=None
		if self.env.OS=='lin' or self.env.OS=='mac':cmd="rm -rf %s"%(fname)
		else:cmd="del %s"%(fname)
		if DEBUG:print cmd
		try:os.system(cmd)
		except:pass#print 'unable to recursively delete 2x',fname
		
		self.reload('new')


	def saveCB(self,evt):
		
		if DEBUG:print 'saveCB'
		#check for USERNAME='new'; here/this is the only filter.
		for obj in self.cfgctrlobjs:
			if obj.key=='USERNAME':
				if str(obj.widget.GetValue())=='new':return
			elif obj.key=='PROFILE_NAME':
				if str(obj.widget.GetValue())=='default':return
		
		#update fields w/assoc ctrl widgets
		for obj in self.cfgctrlobjs:
			obj.update()#widget.value -> obj.val['value']
			key=obj.key
			val=obj.val
			self.global_config[key]=val
			if key=='USERNAME':self.global_config['CFGNAME']=val['value']
			elif key=='PROFILE_NAME':self.global_config['PROFILE_NAME']=val['value']
		
		if self.global_config.has_key('letters'):del self.global_config['letters']
		if self.global_config.has_key('distribution'):del self.global_config['distribution']
		if self.global_config.has_key('scoring'):del self.global_config['scoring']
		
		
		oufdir=os.path.join(self.env.configdir,self.tab_name,self.global_config['CFGNAME'])
		if not os.path.exists(oufdir):return#returns on GPL and Asymptopia (continues for Globals)
		oufname=os.path.join(oufdir,'config')
		ouf=open(oufname,'w')
		rval=format_dict(self.global_config,0)
		ouf.write(rval)
		ouf.close()

		try:
			#self.reload(self.global_config['CFGNAME'])#BUG 121907
			self.reload_configs()
		except Exception,e:
			if DEBUG:print e
		
		if DEBUG:print 'saveCB done.'
		
	
	def reload_configs(self):
		if DEBUG:print 'CfgCtrl.reload_configs'
		self.parent.reload_configs()
		self.global_config=self.parent.global_config
		
			
	def load_selected(self,evt):
		
		#load the selected config
		if self.tab_name=='Globals':
			target='globals'#self.cb.GetValue()
		elif self.tab_name=='Readme':
			target='Readme'
		elif self.tab_name=='GPL':
			target='GPL'
		elif self.tab_name=='Asymptopia':
			target='Asymptopia'
			
		sitepkgdir=self.env.sitepkgdir
		configdir=self.env.configdir
		self.cfg=self.global_config#self.load_config(os.path.join(self.tab_name,target),'config')
		
		#clear/delete? self.ControlPanel
		if self.cp!=None:
			self.cp.DestroyChildren()
			self.sizer.Remove(self.cp)
			del self.cp
			self.cp=None
		
		#re-create ControlPanel:
		self.cfgctrlobjs=[]
		W=self.global_config['WIN_W']['value']-self.global_config['SPLITTER_OFFSET']['value']-100
		H=self.global_config['WIN_H']['value']
		cpID=wx.NewId()
		
		
		if target=='globals':
			self.cp=scrolled.ScrolledPanel(self,wx.NewId(),wx.DefaultPosition,style=wx.FULL_REPAINT_ON_RESIZE|wx.ALWAYS_SHOW_SB|wx.VSCROLL)
			self.reload_configs()
			if target=='globals':
				self.cp.SetBackgroundColour(self.global_config['COLOR_BG_ADMIN']['value'])
				self.cp.SetForegroundColour(self.global_config['COLOR_FG_ADMIN']['value'])
			
			cpsizer=wx.BoxSizer(wx.VERTICAL)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)
			#staticbox widgets into a vertical box sizer

			keys=self.cfg.keys()
			keys.sort()
			for idx in range(len(keys)):
				item=keys[idx]
				if type(self.cfg[item])!=types.DictType:continue
				if not self.cfg[item].has_key('showme'):continue
				if self.cfg[item]['showme'] or self.SHOW_ALL:
					cpobj=CfgCtrlObj(self.cp,item,self.cfg[item],self.global_config,self.env)
					cpsizer.Add(cpobj.sizer,0,wx.GROW,1)
					self.cfgctrlobjs.append(cpobj)#need this still?
			
			self.cp.SetSizer(cpsizer)
			self.cp.SetAutoLayout(True)
			self.Layout()
			self.cp.Layout()
			self.cp.Refresh()
			
			self.cp.SetupScrolling()
			self.cp.SetScrollRate(10,10)

		
		elif target=='Readme':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.env.sitepkgdir,self.cfg['APPNAME'],'README'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print dir(editor)
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)

		elif target=='GPL':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.env.sitepkgdir,self.cfg['APPNAME'],'LICENSE'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print dir(editor)
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)
			

		elif target=='Asymptopia':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.env.sitepkgdir,self.cfg['APPNAME'],'ASYMPTOPIA'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print dir(editor)
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)
			
		
	def scrollCB(self,evt):
		if DEBUG:print 'scrollCB'
		
	def load_config(self,intermediate_path,fname):
		
		sitepkgdir	=self.env.sitepkgdir
		configdir	=self.env.configdir
		if DEBUG:print configdir,intermediate_path,fname
		infname=os.path.join(configdir,intermediate_path,fname)
		inf=open(str(infname))
		content=inf.read()
		
		#NEED:re-format tripple-quoted multiline strings
		content=string.strip(content)
		if DEBUG:print content
		
		config=eval(content)
		inf.close()
		return config

	def reload(self,name):
		#installed=self.get_installed()
		#for idx in range(len(installed)):
		#	self.cb.Append(installed[idx])
		self.load_selected(None)

	def get_installed(self):
		fnames=os.listdir(os.path.join(self.env.configdir,self.tab_name))
		rnames=[]
		for f in fnames:
			if f=='__init__.py':continue
			rnames.append(f)
		return rnames

	def logoutCB(self,e):
		#type(self.parent)=wxDialog
		self.parent.EndModal(0)
		
	def showallCB(self,e):
		if self.SHOW_ALL==1:self.SHOW_ALL=0
		else:self.SHOW_ALL=1
		self.load_selected(None)
		if DEBUG:print 'SHOW_ALL=',self.SHOW_ALL
