#!/usr/bin/env python
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
import os,sys,string,time
from TuxWordSmith.tws import *

def usage():
	msg="""
Usage: tuxwordsmith [OPTION]
	Available options are:
	-help				Show this help
	-wx				Enable the wx admin interface
	-d <dictionary>			Use specified dictionary

Example:
	./tuxwordsmith -d Spanish-English
	
For additional languages, follow the download link at
http://www.asymptopia.org for extra languages and unzip
each additional language to the xdxf directory appropriate
to your installation.	
	"""
	print msg
	
if __name__ == "__main__":
	appdir='TuxWordSmith'
	if len(sys.argv)==1:
		x=TuxWordSmithApp()
	elif sys.argv[1]=='-help':
		usage()
	elif sys.argv.count('-wx')>0:
		from TuxWordSmith.tws_wx import *
		x=TuxWordSmithAppWX()
	else:
		x=TuxWordSmithApp()
