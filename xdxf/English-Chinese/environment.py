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
import os,sys,string

class Environment:
	def __init__(self,appname):
		self.OS=None
		OS=string.lower(sys.platform)
		if string.find(OS,'win')>-1:OS='win'
		elif string.find(OS,'mac')>-1:OS='mac'
		elif string.find(OS,'lin')>-1:OS='lin'
		else:OS=None
		if(OS==None):sys.exit()
		
		if(OS==('lin' or 'mac')):
			import pygame 
			for sitepkgdir in sys.path:
				if sitepkgdir[-13:]=='site-packages':break
			configdir=os.path.join('/','var','games',appname)#,os.path.basename(appname)
			userdir=os.path.join(configdir,'Accounts')
			homedir=os.getenv('HOME')
		
		elif OS=='win':
			import thread
			pf=os.getenv("PROGRAMFILES")
			sitepkgdir=os.path.join(pf,appname)
			userdir=os.path.join(sitepkgdir,appname,"Accounts")
			configdir=os.path.join(sitepkgdir,appname)
			homedir=os.getenv('HOME')
			
		
		self.OS=OS
		self.sitepkgdir=sitepkgdir
		self.userdir=userdir
		self.configdir=configdir
		self.appname=appname
		self.homedir=homedir
				
		"""
		print 'configdir   =%s'%self.configdir
		print 'userdir     =%s'%self.userdir
		print 'sitepkgdir  =%s'%self.sitepkgdir
		print 'appname     =%s'%self.appname
		print 'homedir     =%s'%self.homedir
		"""
