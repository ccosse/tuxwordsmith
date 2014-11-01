#!/usr/bin/python
# -*- coding: UTF-8 -*-

from asymptopia_0_1_3.xdxf_parser import *
from asymptopia_0_1_3.letters import *
from asymptopia_0_1_3.line_formatter import *

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
		
		
		
		new_key=dh.kadict[key]
		new_content=key
		
		line="<ar><k>"+new_key.encode('UTF-8')+"</k>"
		ouf.write(line)
		
		line=new_content.encode('UTF-8')+"</ar>\n"
		ouf.write(line)
		
		print "%d/%d"%(wc,num_words)

	except Exception,e:
		print wc,e

		
inf.close()
ouf.close()
