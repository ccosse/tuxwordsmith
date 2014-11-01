#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xdxf_parser import *
from letters import *
from line_formatter import *

inf=open('dict.xdxf')
ouf=open('dflip2.xdxf','w')
dh=GetKeyArticleDict('ALL')
parser.setContentHandler(dh)
parser.parse(inf)
inf.seek(0)


wc=0

#available_words=dh.keys#list
#num_words=len(available_words)

#for word in available_words:
keys=dh.kadict.keys()
num_words=len(keys)
for key in keys:
	try:
		wc+=1
		#dh=GetArticle(word)
		#parser.setContentHandler(dh)
		#inf.seek(0)
		#parser.parse(inf)
		#article=dh.article
		
		
		pinying=string.split(dh.kadict[key],']',1)[0]
		pinying=string.replace(pinying,'[','')
		
		new_keys=string.split(dh.kadict[key],']',1)[1]
		new_keys=string.split(new_keys,'/',10)
		new_keys.pop(0)
		new_keys.pop()
		
		#print new_keys
		#new_key=dh.kadict[key]
		
		new_content=key+" ["+pinying+"]"

		for new_key in new_keys:
		
			line="<ar><k>"+new_key.encode('UTF-8')+"</k>"
			print line
			ouf.write(line)
			
			line=new_content.encode('UTF-8')+"</ar>\n"
			print line
			ouf.write(line)
		
		print "%d/%d"%(wc,num_words)

	except Exception,e:
		print wc,e

		
inf.close()
ouf.close()
