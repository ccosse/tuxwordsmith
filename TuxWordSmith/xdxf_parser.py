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
import xml,sys,os,string,unicodedata,time
from random import random

from xml.sax import make_parser
from xml.sax import saxutils
from xml.sax.handler import feature_namespaces

DEBUG=False
#DEBUG=1

letters=['"','&',';',':','?','<','>',' ','-','.','/','"','(',')',"'",'{','}','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
	u'\xe0',# à
	u'\xe1',# á
	u'\xe2',# â
	u'\xe3',# ã
	u'\xe4',# ä
	u'\xe6',# æ
	u'\xe7',# ç
	u'\xe8',# è
	u'\xe9',# é
	u'\xee',# î
	u'\xef',# ï
	u'\xed',# í
	u'\xeb',# ë
	u'\xea',# ê
	u'\xf1',# ñ
	u'\xf3',# ó
	u'\xf4',# ô
	u'\xf6',# ö
	u'\xf9',# ù
	u'\xfa',# ú
	u'\xfb',# û
	u'\xfc',# ü
]
#RUSSIAN
hexnames=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
for idx in range(04,05):
	for hdx1 in range(3,6):
		for hdx2 in range(0,16):
			ustr="u\'\\u%02d%c%c\'"%(idx,hexnames[hdx1],hexnames[hdx2])
			letters.append(eval(ustr))
#GREEK
for idx in range(03,04):
	for hdx1 in range(7,16):
		for hdx2 in range(0,16):
			ustr="u\'\\u%02d%c%c\'"%(idx,hexnames[hdx1],hexnames[hdx2])
			letters.append(eval(ustr))


def lower_uchar(uchar):
	
	uchar_name=None
	
	try:uchar_name=unicodedata.name(uchar)
	except Exception,e:
		#print e,type(uchar),uchar.encode('UTF-8')
		#rval=raw_input('q?')
		#if rval=='q':sys.exit()
		return uchar
	
	modified_uchar_name=string.replace(uchar_name,'CAPITAL','SMALL')
	modified_uchar=unicodedata.lookup(modified_uchar_name)
	return modified_uchar

def upper_uchar(uchar):
	
	uchar_name=None
	
	try:uchar_name=unicodedata.name(uchar)
	except Exception,e:
		#print e,uchar,uchar.encode('UTF-8')
		return uchar
	
	modified_uchar_name=string.replace(uchar_name,'SMALL','CAPITAL')
	modified_uchar=unicodedata.lookup(modified_uchar_name)
	return modified_uchar

	
class XDXFParser(xml.sax.ContentHandler):

	def __init__(self):
		
		self.inKey=False
		self.in_arContent=False
		self.inCo=False
		self.inB=False#Etymology
		self.inC=False#PartOfSpeech
		self.inI=False#
		self.inKref=False#
		self.inDtrn=False#Definition
		
		self.SKIPFLAG=False
		
		self.key=None
		self.etymology=None
		self.part_of_speech=None
		self.defn=None
		
		self.content=''

		self.ar_count=0
		self.k_count=0
		self.keys=[]
		self.dict={}
		
		self.indices=[0,0,1000,1000]
		self.tstart=time.time()
		self.tend=self.tstart
		

	def error(self, exception):
		if DEBUG:print exception
	
	def normalize_whitespace(self,text):
		"Remove redundant whitespace from a string"
		return ' '.join(text.split())

	def startElement(self,name,attrs):
		if name=='ar':
			self.in_arContent=True
		elif name=='k':
			self.inKey=True
		elif name=='co':
			self.inCo=True
		elif name=='c':
			self.inC=True
		elif name=='i':
			self.inI=True
		elif name=='b':
			self.inB=True
		elif name=='dtrn':
			self.inDtrn=True
		elif name=='kref':
			self.inKref=True
		
		
	def characters(self,ch):
		if self.inKey:
			self.key=ch
			self.content=''
			if len(ch.split())>1:self.SKIPFLAG=True
			if string.find(ch,'-')>-1:self.SKIPFLAG=True
			
		elif self.inI and ch=='abbreviation':
			self.SKIPFLAG=True
		
		elif self.inI and ch=='name':
			self.SKIPFLAG=True
		
		elif self.inI and ch=='biographical name':
			self.SKIPFLAG=True
			
		elif self.inI and ch=='Biographical name':
			self.SKIPFLAG=True
			
		elif self.inI and ch=='geographical name':
			self.SKIPFLAG=True

		elif self.inI and ch=='Geographical name':
			self.SKIPFLAG=True

		else:
			self.content="%s%s"%(self.content,ch)
				
			"""
			try:print ch
			except Exception,e:
				ordstr=""
				for xidx in range(len(ch)):
					try:ordstr="%s%c"%(ordstr,ord(ch[xidx]))
					except Exception,ee:self.SKIPFLAG=True
				print ordstr
			"""
		
		
		
	def endElement(self,name):
		if name=='ar':
			self.in_arContent=False
			if not self.SKIPFLAG:
				#Build the entry:	
				self.dict[self.key]=self.content
				self.keys.append(self.key)
			
			self.inKey=False
			self.in_arContent=False
			self.inCo=False
			self.inB=False#Etymology
			self.inC=False#PartOfSpeech
			self.inI=False#
			self.inKref=False#
			self.inDtrn=False#Definition
			
			self.SKIPFLAG=False
			
			self.key=None
			self.etymology=None
			self.part_of_speech=None
			self.defn=None
			self.content=None
			
		if name=='k':
			self.inKey=False	
			#self.key=self.normalize_whitespace(self.current_key)
			
		if name=='co':
			self.inCo=False
		if name=='c':
			self.inC=False
		if name=='i':
			self.inI=False
		if name=='b':
			self.inB=False
		if name=='dtrn':
			self.inDtrn=False
		if name=='kref':
			self.inKref=False
		
		
	def display_info(self):
		
		keys=self.dict.keys()
		#print self.dict
		
		for dummy in range(10):
			idx=int(random()*len(keys))
			
			key=keys[idx]
			ch=key
			try:print ch,
			except Exception,e:
				ordstr=""
				for xidx in range(len(ch)):
					try:ordstr="%s%c"%(ordstr,ord(ch[xidx]))
					except Exception,ee:self.SKIPFLAG=True
				print ordstr,
			
			
			ch=self.dict[key]
			try:print ch
			except Exception,e:
				ordstr=""
				for xidx in range(len(ch)):
					try:ordstr="%s%c"%(ordstr,ord(ch[xidx]))
					except Exception,ee:self.SKIPFLAG=True
				print ordstr
			
			print '\n'
			
		print "len(keys):\t%d"%(len(keys))
		print "Time2Load: %6.2f [s]"%(time.time()-self.tstart)
		
		#GetCharacters:
		charset=[]
		for key in keys:
			for cidx in range(len(key)):
				try:kidx=charset.index(key[cidx])
				except:charset.append(key[cidx])
		charset.sort()
		try:print charset
		except Exception,e:print e
		
		print len(charset)

parser = make_parser()
