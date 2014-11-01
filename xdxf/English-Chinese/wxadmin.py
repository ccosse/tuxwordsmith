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
import os,sys,string,time
#from wxPython.wx import *
import wx
from cfgctrl import *

DEBUG=0

class wxAdmin(wx.Dialog):
	
	def __init__(self,parent):
		
		self.lhp_gif=None
		self.splitter=None
		self.simulator=None
		
		self.parent		=parent
		self.env		=parent.env
		self.configdir	=self.env.configdir
		self.userdir	=self.env.userdir
		self.sitepkgdir	=self.env.sitepkgdir
		self.homedir	=self.env.homedir
		self.global_config=self.parent.global_config
		
		wx.Dialog.__init__(self,None,wx.NewId(),self.global_config['APPNAME'],size=wx.Size(800,600),style=wx.RESIZE_BORDER|wx.CAPTION|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX)

	def reload_configs(self):
		self.parent.reload_configs()
		self.global_config=self.parent.global_config
		
	
	def setup(self):
		self.splitter = wx.SplitterWindow (self,wx.NewId(),style=wx.NO_3D)#|wxSP_3D
		self.splitter.SetMinimumPaneSize(self.global_config['SPLITTER_OFFSET']['value'])
		box		=wx.BoxSizer(wx.HORIZONTAL)
		box.Add(self.splitter,1,wx.EXPAND)#0~expand horizontally, 1~expand both directions.
		self.SetSizer(box)
		self.SetAutoLayout(True)
		
		
		self.lhp_gif=None
		lhp=wx.Panel(self.splitter,wx.NewId())
		self.setuplhp(lhp)
		
		rhp=wx.Panel(self.splitter,wx.NewId())
		self.rm=None
		
		tws_tabs=['Globals']
		self.setuprhp(rhp,tws_tabs)
		
		
		self.Centre()
		self.Refresh(True)
		self.splitter.UpdateSize()

		box.Layout()
	
		if self.lhp_gif:self.splitter.SplitVertically(lhp,rhp,self.global_config['SPLITTER_OFFSET']['value'])
		else:self.splitter.SplitVertically(lhp,rhp,lhp.GetWidth())
		self.splitter.UpdateSize()
		
		box.Layout()
		
	def setuplhp(self,lhp):
		lhp.SetSize((self.global_config['SPLITTER_OFFSET']['value'],600))
		lhp.SetBackgroundColour((255,255,255))
		sidebar_fname=self.parent.global_config['IMAGE_ADMIN_SIDEBAR']['value']
		sidebar_fname=os.path.join(self.sitepkgdir,self.parent.global_config['APPNAME'],'Images',sidebar_fname)
		lhp_gif=wx.Image(sidebar_fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap()
		wx.StaticBitmap(lhp,wx.NewId(),lhp_gif,(0,0))
		self.lhp_gif=lhp_gif
		
		
	def setuprhp(self,rhp,tabs):
		
		if DEBUG:print 'wxAdmin::setuplhp'
		gp=None
		nb=wx.Notebook(rhp,wx.NewId(),style=wx.NB_TOP|wx.NB_FIXEDWIDTH)
		
		
		box=wx.BoxSizer(wx.VERTICAL)

		box.Add(nb,1,wx.EXPAND)#0~expand horizontally, 1~expand both directions.

		#tabs=['Accounts','Globals','StudentData','Simulation']#,'GPL'
		for idx in range(0,len(tabs)):
			if tabs[idx]=='Resources':
				mode=0#panel child of parent (nb)
				rm=ResourceManager(self,nb,mode,None,font,300,300,tabs[idx],self.parent.env,self.parent.global_config)
				rm.setup()
				nb.AddPage(rm,tabs[idx],0)
				#self.accounts_editor=rm.editor
				rmbox=wx.BoxSizer(wx.VERTICAL)
				rmbox.Add(rm.toolbar,0,wx.EXPAND)
				rmbox.Add(rm.alb,1,wx.GROW,1)#alb=article list box
				rm.SetSizer(rmbox)
				rm.SetAutoLayout(True)
				self.rm=rm
				
			elif tabs[idx]=='Accounts':
				p=CfgCtrl(self,nb,tabs[idx])
				p.setup()
				nb.AddPage(p,tabs[idx],0)
			elif tabs[idx]=='Globals':
				gp=CfgCtrl(self,nb,tabs[idx])
				gp.setup()
				nb.AddPage(gp,tabs[idx],0)
			elif tabs[idx]=='StudentData':
				p=CfgCtrl(self,nb,tabs[idx])
				p.setup()
				nb.AddPage(p,tabs[idx],0)
			elif tabs[idx]=='Simulation':
				p=Simulator(self,nb,tabs[idx])
				p.setup()
				nb.AddPage(p,tabs[idx],0)
			elif tabs[idx]=='GPL':
				p=CfgCtrl(self,nb,tabs[idx])
				p.setup()
				nb.AddPage(p,tabs[idx],0)
		
		if self.rm!=None:
			self.rm.set_accounts_panel(gp)
			
		rhp.SetSizer(box)
		rhp.SetAutoLayout(True)
