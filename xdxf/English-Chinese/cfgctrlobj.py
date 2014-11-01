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

import  wx.lib.imagebrowser as ib

DEBUG=0

class CfgCtrlObj:
	
	def __init__(self,parent,key,val,global_config,env):
		if DEBUG:print key,val
		self.parent=parent
		self.env=env
		self.key=key
		self.val=val
		self.global_config=global_config
		self.env=env
		
		WIDGET_W=global_config['CONFIG_WIDGET_W']['value']
		WIDGET_H=global_config['CONFIG_WIDGET_H']['value']
		self.wsize=wx.Size(WIDGET_W,WIDGET_H)
		
		self.sbox=wx.StaticBox(self.parent,-1,key,style=wx.BORDER_STATIC)
		self.sbox.SetWindowStyle(wx.BORDER_NONE)
		
		self.sizer=wx.StaticBoxSizer(self.sbox,wx.HORIZONTAL)
		self.widget=None
		self.label=None
		self.defaultB=None
		self.showColourDialogB=None
		self.defaultBID=wx.NewId()
		self.set=0
		self.bmp=None
		
		#every CfgCtrlObj has a defaultB:
		self.defaultB=wx.Button(self.parent,self.defaultBID,"Default",size=self.wsize)
		
		if self.val['wtype']=='wx.ComboBox':
			cbID=wx.NewId()
			cb=wx.ComboBox(self.parent,cbID,size=self.wsize,choices=[])
			for idx in range(len(self.val['default'])):
				cb.Append(self.val['default'][idx])
			cb.SetValue(self.val['value'])
			self.widget=cb
				
			#self.widget.SetValue(self.val['value'])
			self.sizer.Add(self.widget)
			wx.EVT_COMBOBOX(self.parent,cbID,self.comboCB)
			
			if self.val['icon']:
				#in this version, if icon, then actor.
				fname=os.path.abspath(os.path.join(self.env.sitepkgdir,global_config['APPNAME'],'Actors',self.val['value'],'icon.gif'))
				gif=wx.Image(fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap()
				self.bmp=wx.StaticBitmap(self.parent,-1,gif)#,size=wx.Size(WIDGET_W,WIDGET_W)
				self.sizer.Add(self.bmp)
			else:
				self.label=wx.StaticText(self.parent,wx.NewId(),'',size=self.wsize)
				self.sizer.Add(self.label)

			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)

		elif self.val['wtype']=='wx.TextCtrl':
			self.widget=wx.TextCtrl(self.parent,wx.NewId(),style=self.val['style'],size=self.wsize)
			self.widget.SetValue(self.val['value'])
			self.widget.SetLabel(self.val['descr'])
			self.sizer.Add(self.widget)
			
			label_str=''
			self.label=wx.StaticText(self.parent,wx.NewId(),label_str,size=self.wsize)
			self.sizer.Add(self.label)

			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)
			
		elif self.val['wtype']=='wx.ImageDialog':
			ImgBrowserID=wx.NewId()
			self.widget=ib.ImageDialog(
				self.parent,
				self.val['path'],
			)
			
			ibID=wx.NewId()
			self.ibB=wx.Button(self.parent,ibID,"ImageDialog",size=self.wsize)
			self.sizer.Add(self.ibB)
			wx.EVT_BUTTON(self.ibB,ibID,self.imagedialogCB)
			
			label_str=''
			self.label=wx.StaticText(self.parent,wx.NewId(),label_str,size=self.wsize)
			self.label.SetLabel(self.val['value'])
			self.sizer.Add(self.label)

			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)
		
		elif self.val['wtype']=='wx.FileDialog':
			
			FileDialogID=wx.NewId()
			self.widget=wx.FileDialog(
				self.parent,
				message="Choose file",
				defaultDir=self.val['path'],
			)
			
			fdID=wx.NewId()
			self.fdB=wx.Button(self.parent,fdID,"ShowDialog",size=self.wsize)
			self.sizer.Add(self.fdB)
			wx.EVT_BUTTON(self.fdB,fdID,self.filedialogCB)
			
			label_str=''
			self.label=wx.StaticText(self.parent,wx.NewId(),label_str,size=self.wsize)
			self.label.SetLabel(self.val['value'])
			self.sizer.Add(self.label)

			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)

			
			
		elif self.val['wtype']=='wx.CheckBox':
			CheckBoxID=wx.NewId()
			self.widget=wx.CheckBox(self.parent,CheckBoxID,"",size=self.wsize)
			self.widget.SetValue(int(self.val['value']))
			self.sizer.Add(self.widget)
			wx.EVT_CHECKBOX(self.widget,CheckBoxID,self.checkboxCB)
		
			label_str=''
			self.label=wx.StaticText(self.parent,wx.NewId(),label_str,size=self.wsize)
			self.label.SetLabel(`self.val['value']`)
			self.sizer.Add(self.label)

			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)

			self.checkboxCB(None)#to set the label after label exists
			
		elif self.val['wtype']=='wx.SpinCtrl':
			SpinCtrlID=wx.NewId()
			self.widget=wx.SpinCtrl(self.parent,SpinCtrlID,size=self.wsize)
			self.widget.SetRange(self.val['min'],self.val['max'])
			self.widget.SetValue(int(self.val['value']))
			self.sizer.Add(self.widget)
			wx.EVT_SPINCTRL(self.widget,SpinCtrlID,self.spinctrlCB)
			
			label_str=''
			self.label=wx.StaticText(self.parent,wx.NewId(),label_str,size=self.wsize)
			self.label.SetLabel(`self.val['value']`)
			self.sizer.Add(self.label)

			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)
			
			
		elif self.val['wtype']=='wx.ColourDialog':
			
			self.widget=wx.ColourDialog(self.parent)
			self.widget.GetColourData().SetChooseFull(True)
			self.widget.GetColourData().SetColour(wx.Colour(self.val['value'][0],self.val['value'][1],self.val['value'][2]))
			
			showColourDialogBID=wx.NewId()
			self.showColourDialogB=wx.Button(self.parent,showColourDialogBID,"ShowDialog",size=self.wsize)
			self.showColourDialogB.SetBackgroundColour(self.widget.GetColourData().GetColour().Get())
			self.sizer.Add(self.showColourDialogB)
			wx.EVT_BUTTON(self.showColourDialogB,showColourDialogBID,self.showColourDialogCB)
			
			label_str=''
			self.label=wx.StaticText(self.parent,wx.NewId(),label_str,size=self.wsize)
			self.label.SetLabel(`self.val['value']`)
			self.sizer.Add(self.label)

			self.defaultB.SetBackgroundColour(self.val['default'])
			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)
			
		elif self.val['wtype']=='wx.Slider':
			
			self.widget=wx.Slider(
				self.parent,
				wx.NewId(),
				int(self.val['value']*self.val['divisor']),
				int(self.val['min']),
				int(self.val['max']),
				style=self.val['style'],
				size=self.wsize
			)
			
			
			self.sizer.Add(self.widget)

			sliderID=wx.NewId()
			div=self.val['divisor']
			if div==1.:label_str="%.0f"%(self.val['value'])
			if div==10.:label_str="%.1f"%(self.val['value'])
			if div==100.:label_str="%.2f"%(self.val['value'])
			if div==1000.:label_str="%.3f"%(self.val['value'])
			if div==10000.:label_str="%.4f"%(self.val['value'])
			
			self.label=wx.StaticText(self.parent,sliderID,label_str,size=self.wsize)
			self.sizer.Add(self.label)
			
			wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)
			wx.EVT_SCROLL(self.widget,self.sliderCB)
		
		self.sizer.Add(self.defaultB)
		if self.val.has_key('tooltip'):
			if DEBUG:print self.val
			self.defaultB.SetToolTip(wx.ToolTip(self.val['tooltip']))
			
	def comboCB(self,evt):
		newval=self.widget.GetValue()
		if DEBUG:print 'comboCB:',newval
		if self.val['icon']:
			fname=os.path.abspath(os.path.join(self.env.sitepkgdir,self.global_config['APPNAME'],'Actors',newval,'icon.gif'))
			self.bmp.SetBitmap(wx.Image(fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap())
		
		
	def imagedialogCB(self,evt):
		if self.widget.ShowModal()==wx.ID_OK:
			fname=self.widget.GetFile()
			self.val['value']=str(os.path.basename(fname))
			self.label.SetLabel(self.val['value'])
			
	def filedialogCB(self,evt):
		if self.widget.ShowModal()==wx.ID_OK:
			path=self.widget.GetPaths()[0]
			self.val['path']=str(os.path.dirname(path))
			self.val['value']=str(os.path.basename(path))
			self.label.SetLabel(self.val['value'])
			
	def checkboxCB(self,evt):
		if self.widget.GetValue():value_str="On"
		else:value_str="Off"
		self.label.SetLabel(value_str)

	def spinctrlCB(self,evt):
		value_str="%02d"%(self.widget.GetValue())
		self.label.SetLabel(value_str)
	
	def sliderCB(self,evt):
		if DEBUG:print 'sliderCB: ',self.widget.GetValue()
		div=self.val['divisor']
		if div==1.:label_str="%.0f"%(self.widget.GetValue()/self.val['divisor'])
		if div==10.:label_str="%.1f"%(self.widget.GetValue()/self.val['divisor'])
		if div==100.:label_str="%.2f"%(self.widget.GetValue()/self.val['divisor'])
		if div==1000.:label_str="%.3f"%(self.widget.GetValue()/self.val['divisor'])
		if div==10000.:label_str="%.4f"%(self.widget.GetValue()/self.val['divisor'])
		self.label.SetLabel(label_str)
	
	def defaultCB(self,evt):
		
		#print dir(self.parent)
		self.parent.Layout()
		
		if self.val['wtype']=='wx.ComboBox':
			self.widget.SetValue(self.val['value'])
			self.comboCB(None)
			
		elif self.val['wtype']=='wx.TextCtrl':
			self.widget.SetValue(self.val['default'])
			
		elif self.val['wtype']=='wx.Slider':
			self.widget.SetValue(int(self.val['default']*self.val['divisor']))
			self.sliderCB(None)
			
		elif self.val['wtype']=='wx.ImageDialog':
			self.val['value']=self.val['default']
			self.label.SetLabel(self.val['value'])

		elif self.val['wtype']=='wx.FileDialog':
			self.val['value']=self.val['default']
			self.label.SetLabel(self.val['value'])

		elif self.val['wtype']=='wx.ColourDialog':
			self.val['value']=self.val['default']
			self.label.SetLabel(`self.val['value']`)
			self.widget.GetColourData().SetColour(self.val['value'])
			self.showColourDialogB.SetBackgroundColour(self.val['value'])

		elif self.val['wtype']=='wx.SpinCtrl':
			self.widget.SetValue(int(self.val['default']))
			self.spinctrlCB(None)
		
		elif self.val['wtype']=='wx.CheckBox':
			self.widget.SetValue(int(self.val['default']))
			self.checkboxCB(None)
	
	def showColourDialogCB(self,evt):
		if self.widget.ShowModal()==wx.ID_OK:pass
		else:return
		self.label.SetLabel(`self.val['value']`)		
		self.showColourDialogB.SetBackgroundColour(self.widget.GetColourData().GetColour().Get())
				
	def update(self):
		if self.val['wtype']=='wx.ComboBox':
			self.val['value']=str(self.widget.GetValue())
			
		elif self.val['wtype']=='wx.TextCtrl':
			self.val['value']=str(self.widget.GetValue())
			
		elif self.val['wtype']=='wx.ImageDialog':
			#self.val['value']=os.path.basename(self.widget.GetFile())
			if DEBUG:print 'value=',self.val['value'],self.label.GetLabel()
			
			"""
		elif self.val['wtype']=='wx.FileDialog':
			try:
				self.val['path']=str(os.path.dirname(self.widget.GetPaths()[0]))
				self.val['value']=str(os.path.basename(self.widget.GetPaths()[0]))
				if DEBUG:print 'path=',self.val['path']#,self.label.GetLabel()
				if DEBUG:print 'value=',self.val['value']#,self.label.GetLabel()
			except Exception,e:
				print 'Line 288 cfgctrlobj.py: ',e
			"""
			
		elif self.val['wtype']=='wx.SpinCtrl':
			self.val['value']=int(self.widget.GetValue())#was float
			if DEBUG:print 'value=',self.val['value'],self.label.GetLabel()

		elif self.val['wtype']=='wx.CheckBox':
			self.val['value']=int(self.widget.GetValue())
			if DEBUG:print 'value=',self.val['value'],self.label.GetLabel()

		elif self.val['wtype']=='wx.Slider':
			self.val['value']=float(self.widget.GetValue())/self.val['divisor']#was float
			if DEBUG:print 'value=',self.val['value'],self.label.GetLabel()

		elif self.val['wtype']=='wx.ColourDialog':
			#LEAVE OFF: @default need to SetColourData -- need refer to wx API...TBC.
			data=self.widget.GetColourData()
			self.val['value']=data.GetColour().Get()
			self.label.SetLabel(`self.val['value']`)
		
