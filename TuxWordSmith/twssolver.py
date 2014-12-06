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
import sys,time,os,string,unicodedata,math
from random import random
from xdxf_parser import *

DEBUG=0

class TWSSolver:
	def __init__(self,mode,level):
		if DEBUG:print 'TWSSolver'
		
		#041708: Big change -- keeping persistent dictionary in memory now
		self.dh=None
		
		self.encoding='UTF-8'
		self.env=None
		self.global_config=None
		self.admin=None
		self.players=None
		self.MODE=mode
		self.LEVEL=level
		self.NNUMBERS=None
		self.STOP_RUNNING=0
		
		self.game=self
		self.tray=None
		
		self.fullnames_targets=None
		self.current_resource_key=None
		self.current_resource_path=None
		self.available_words=None
		self.key_count=0
		
		self.special_chars=None
		self.ntuple=None
		self.candidates=None
		
		self.fieldmap={
			'CHARSET':0,
			'CASE':1,
			'DESCRIPTOR':2,
			'VALUE':3,
			'PREPOSITION':4,
			'MOD':5,
		}
		

		
	def get_installed(self):
		self.fullnames_targets={}
		dnames=os.listdir(os.path.join(self.env.configdir,'xdxf'))
		return dnames
	
	def load_resource(self):	

		if DEBUG:print 'load_resource',self.current_resource_key
		self.global_config['letters']=[]
		self.global_config['distribution']={}
		self.global_config['scoring']={}
		
		target=os.path.join(self.env.configdir,'xdxf',self.current_resource_key,'dict.xdxf')
		if not target:return
		
		self.current_resource_path=target
		
		msg="... %s ..."%(self.current_resource_key)
		self.progress_message(msg)
		
		inf=open(target)
		#dh=GetKeys('ALL')#self.current_letter
		#parser.setContentHandler(dh)
		
		self.dh=XDXFParser()
		parser.setContentHandler(self.dh)
		
		parser.parse(inf)
		inf.close()
		if DEBUG:print len(self.dh.keys)
		if DEBUG:print self.dh.keys
		
		#self.dh.display_info()
		
		#self.available_words=dh.keys#list
		self.available_words=self.dh.keys#list
		
		self.key_count=len(self.available_words)
		
		
		#101607:creating charset here:
		use_lower=1#self.global_config['GAME_TILES_USE_LOWER_CASE']['value']
		numwords_total=len(self.available_words)		
		wordcount=0
		throw_away_count=0
		salvage_count=0
		words=[]
		for word in self.available_words:
			#added:070808
			if not word:continue
			
			OMIT_FLAG=0
			
			word=string.replace(word,',','')
			word=string.replace(word,'.','')
			word=string.replace(word,'-',' ')
			word=string.replace(word,'!',' ')
			word=string.replace(word,'?',' ')
			
			#strip-out parentheses:
			lidx=None;ridx=None
			if word.count('('):
				lidx=word.index('(')
				if word.count(')'):
					ridx=word.index(')')
					word=word[:lidx]+u' '+word[ridx+1:]
			
			case_word=u''
			for uchar in word:#NEED:move this to separate func so can call 2x -- 2nd time is with salvaged words
				
				#added 070708 b/c some dflip dicts 
				try:
					uname=unicodedata.name(uchar)
				except:continue
				
				if uname=='SPACE':OMIT_FLAG=1
				
				#02/07/2008 - Prevent characters with unicode modifications in English-AnyLang mode:
				elif (self.current_resource_key[:8]=='English-' and string.find(uname,'WITH')>=0):
					if DEBUG:print self.current_resource_key[:8],uname
					OMIT_FLAG=2
				
				#04/17/2008 - Prevent characters with unicode modifications in English-AnyLang mode:
				elif (self.current_resource_key[:8]=='Merriam-' and string.find(uname,'WITH')>=0):
					if DEBUG:print self.current_resource_key[:8],uname
					OMIT_FLAG=2
				elif (self.current_resource_key[:8]=='Merriam-' and string.find(uname,'AE')>=0):
					if DEBUG:print self.current_resource_key[:8],uname
					OMIT_FLAG=2
				elif (self.current_resource_key[:8]=='Merriam-' and string.find(uname,'DOTLESS')>=0):
					if DEBUG:print self.current_resource_key[:8],uname
					OMIT_FLAG=2
				elif (self.current_resource_key[:8]=='Merriam-' and string.find(uname,'LIGATURE')>=0):
					if DEBUG:print self.current_resource_key[:8],uname
					OMIT_FLAG=2
				elif (self.current_resource_key[:8]=='AAA-Oxfo' and string.find(uname,'WITH')>=0):
					if DEBUG:print self.current_resource_key[:8],uname
					OMIT_FLAG=2
				
					
				
				
				#Resource not Cyrillic and uchar not LATIN :
				#also catches spanish special case to remove u-ddot
				elif self.current_resource_key[:8]!='Greek-En' and self.current_resource_key[:8]!='Ukrainia' and self.current_resource_key[:8]!='Russian-':#This hard-coded feature needs to goto documentation!
					if string.find(uname,'LATIN')<0:OMIT_FLAG=2
					elif (self.current_resource_key[:8]=="Spanish-" and string.find(uname,'DIAERESIS')>=0):
						OMIT_FLAG=1
						
				#Resource is Cyrillic and uchar not Cyrillic:
				elif self.current_resource_key[:8]=='Ukrainia' or self.current_resource_key[:8]=='Russian-':
					if string.find(uname,'CYRILLIC')<0:OMIT_FLAG=2
				
				
				
				#Resource is Greek and uchar not Greek:
				elif self.current_resource_key[:8]=='Greek-En':
					#print uname
					if uname=='GREEK TONOS':OMIT_FLAG=2#special case
					elif uname=='GREEK CAPITAL LETTER IOTA WITH DIALYTIKA AND TONOS':OMIT_FLAG=2
					elif uname=='GREEK CAPITAL LETTER UPSILON WITH DIALYTIKA AND TONOS':OMIT_FLAG=2
					elif uname=='GREEK CAPITAL LETTER FINAL SIGMA':OMIT_FLAG=2
					elif uname=='GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS':OMIT_FLAG=2
					elif uname=='GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS':OMIT_FLAG=2
					elif uname=='GREEK SMALL LETTER FINAL SIGMA':OMIT_FLAG=2
					elif string.find(uname,'GREEK')<0:OMIT_FLAG=2
				
				if OMIT_FLAG>0:break
				if use_lower:uname=string.replace(uname,'CAPITAL','SMALL')
				else:uname=string.replace(uname,'SMALL','CAPITAL')
				
				case_word+=unicodedata.lookup(uname)
				
				try:self.global_config['distribution'][uname]+=1
				except:
					if DEBUG:print 'adding:',unicodedata.name(uchar),OMIT_FLAG
					self.global_config['distribution'][uname]=1
					self.global_config['letters'].append(unicodedata.lookup(uname))
					self.global_config['scoring'][uname]=1
			
			if OMIT_FLAG==2:
				if DEBUG:print 'Throwing away: ',`word`
				#msg=u'Throwing away: '+word
				#self.progress_message(msg)
				throw_away_count+=1
				continue
			"""
			elif OMIT_FLAG==1:
				#print 'Separating: ',`word`
				splitword=string.split(word,u' ',10)
				for subword in splitword:
					if self.available_words.count(subword)>0:continue
					if len(subword)>3:
						self.available_words.append(subword)#NEED:we just lost the association with definition! (need to keep Context)
						salvage_count+=1
				continue
			"""
			if not OMIT_FLAG:	
				words.append(case_word)
			
			if math.fmod(wordcount,500)==0:
				msg="wordcount = %7d/%6d"%(wordcount,numwords_total+salvage_count-throw_away_count)
				self.progress_message(msg)
			wordcount+=1

		#
		if DEBUG:pass
		if DEBUG:pass
		if DEBUG:print 'Threw away: ',throw_away_count
		if DEBUG:print 'Salvaged:   ',salvage_count
		if DEBUG:print 'Total:      ',len(words),'/',len(self.available_words)
		
		#IMPORTANT:(trouble popping/removing from existing list--this is a hack!)
		self.available_words=words

		#
		msg="Computing Scoring Scheme..."
		self.progress_message(msg)
		
		
		#101607:
		ctot=0#character total over all channels
		ntot=self.global_config['GAME_TILES_SETSIZE']['value']#num tiles total in set
		minval=self.global_config['GAME_TILE_MIN_VALUE']['value']
		maxval=self.global_config['GAME_TILE_MAX_VALUE']['value']
		vrange=maxval-minval
		
		for uname in self.global_config['distribution']:
			ctot+=self.global_config['distribution'][uname]
		
		#Get max freq of occurance:
		max_freq=0.
		for uname in self.global_config['distribution'].keys():
			self.global_config['distribution'][uname]=int(ntot*self.global_config['distribution'][uname]/ctot)
			self.global_config['distribution'][uname]=max(1,self.global_config['distribution'][uname])
			this_freq=float(self.global_config['distribution'][uname])
			if this_freq>max_freq:max_freq=this_freq
		
		
		#Compute scoring based on relative frequencies of occurance:
		for uname in self.global_config['distribution'].keys():
			this_freq=float(self.global_config['distribution'][uname])
			self.global_config['scoring'][uname]=int(maxval-vrange*this_freq/max_freq)
			if DEBUG:print uname,this_freq,self.global_config['scoring'][uname]
			
		print self.current_resource_key
		for uname in self.global_config['distribution'].keys():
			print uname,self.global_config['distribution'][uname]
			
		#if not self.ntuple:#NEED:Save ntuple across sessions (would require don't re-create tws_solver)
		self.build_ntuple()
		
		
	def build_ntuple(self):
			
			#for idx in range(len(self.global_config['letters'])):
			#	print unicodedata.name(self.global_config['letters'][idx])
			#sys.exit()
			
			self.ntuple={}
			
			distro=[]
			for dummy in range(len(self.global_config['letters'])):distro.append(0)
			
			indices_to_remove=[]
			total_wordcount=len(self.available_words)
			wordcount=0
			for uniword in self.available_words:
				wordcount+=1
				fp_list=self.mkfingerprint(uniword)
				fp_num=self.mkfp_num(fp_list)
				
				if math.fmod(wordcount,100)==0:
					msg="Building Ntuple...%7d/%7d"%(wordcount,total_wordcount)
					self.progress_message(msg)
		
				if self.ntuple.has_key(fp_num):
					self.ntuple[fp_num]['article_lookup_keys'].append(uniword)#raw_word
					self.ntuple[fp_num]['identical_letter_content'].append(uniword)
					
				else:
					
					fp_sum=self.mkfp_sum(fp_list)
					scrabble_sum=self.get_scrabble_sum(fp_list)
							
					self.ntuple[fp_num]={
						'article_lookup_keys':[uniword],
						'identical_letter_content':[uniword],
						'fp_sum':fp_sum,
						'scrabble_sum':scrabble_sum,
						'fp_list':fp_list,
					}
					

	def mkfingerprint(self,uniword):
		
		fingerprint=[]
		
		for idx in range(len(self.global_config['letters'])):fingerprint.append(0)
		
		for idx in range(len(uniword)):
			try:fingerprint[self.global_config['letters'].index(uniword[idx])]+=1
			except Exception,e:return None
				
		return fingerprint

	def get_candidates(self,fp_list,min_wc,max_wc,max_delta):
		
		ntuple=self.ntuple
		candidates=[]
		
		#get wc_candidates with only 1 bit toggled:
		keys=ntuple.keys()
		if DEBUG:print "get_candidates: checking %d records"%len(keys)
		
		for key in keys:
			
			wc_list,delta=self.compute_delta(ntuple[key]['fp_list'],fp_list)
			
			if len(wc_list)<min_wc:continue
			if len(wc_list)>max_wc:continue
			if len(wc_list)>max_delta:continue
			if (delta-len(wc_list))<=max_delta:
				fp_sum=self.mkfp_sum(self.ntuple[key]['fp_list'])
				scrabble_sum=self.get_scrabble_sum(self.ntuple[key]['fp_list'])
				words=ntuple[key]['identical_letter_content']
				article_lookup_keys=ntuple[key]['article_lookup_keys']
				
				if DEBUG:print 'get_candidates: ',words,type(words[0])
				word_list=[]
				key_list=[]
				for idx in range(len(words)):
					word_list.append(words[idx])
					key_list.append(article_lookup_keys[idx])
					
				candidates.append((key,word_list,wc_list,delta-len(wc_list),fp_sum,scrabble_sum,key_list))
				
				
		#sort by scrabble_sum
		for idx0 in range(len(candidates)):
			for idx1 in range(idx0,len(candidates)):
				if candidates[idx1][5]>candidates[idx0][5]:
					tmp1=candidates.pop(idx1)
					tmp0=candidates.pop(idx0)
					candidates.insert(idx0,tmp1)
					candidates.insert(idx1,tmp0)
					
		return candidates
	
	def compute_delta(self,L0,L1):
		delta=0
		fp_diff=self.subtract_fp0_from_fp1(L0,L1)
		delta=0
		wc_list=[]
		for idx in range(len(self.global_config['letters'])):
			if fp_diff[idx]>=0:
				delta+=fp_diff[idx]
			else:
				delta+=abs(fp_diff[idx])
				for xidx in range(abs(fp_diff[idx])):
					wc_list.append(self.global_config['letters'][idx])
		return wc_list,delta
		
	def subtract_fp0_from_fp1(self,fp0,fp1):
		fp=[]
		for idx in range(len(self.global_config['letters'])):
			val=fp1[idx]-fp0[idx]
			fp.append(val)
			#if val<0:print 'val=',val
		
		return fp

	def subtract_strfp0_from_strfp1(self,fp0,fp1):
		fp=[]
		if len(fp0)!=len(fp1):
			if DEBUG:print "ERROR: lists not same length!!"
		for idx in range(len(fp1)):
			
			try:v1=eval(fp1[idx])
			except:v1='--'
			try:v0=eval(fp0[idx])
			except:v0='--'
			
			val=999
			if v0=='--' and v1=='--':val=0
			elif (v0=='--' or v1=='--'):val=-1
			else:val=v1-v0
			
			if val!=0:return None
			
			#print "%s-%s=%d"%(fp1[idx],fp0[idx],val)
			fp.append(val)
		
		return fp
			
	
	def get_unidesc_field(self,uchar,field):
		unidesc=unicodedata.name(uchar)
		unilist=string.split(unidesc,' ',10)
		idx=self.fieldmap[field]
		if len(unilist)>idx:return unilist[idx]
		return None

	def mkfp_num(self,fp_list):
		fp_num=""
		for idx in range(len(fp_list)):
			if fp_list[idx]<0:return None
			fp_num="%s%c"%(fp_num,str(fp_list[idx]))#00102030001002
		return fp_num

	def mkfp_sum(self,fp_list):
		fp_sum=0
		for cidx in range(len(fp_list)):fp_sum+=fp_list[cidx]
		return fp_sum
		
	def get_scrabble_sum(self,fp_list):
		
		gc=self.global_config
		scrabble_sum=0
		for cidx in range(len(fp_list)):#NOTE:ordering of fp_list == ordering of gc['letters'], and NOT alphabetical!
			
			uchar=gc['letters'][cidx]
			letter_score=gc['scoring'][unicodedata.name(uchar)]*fp_list[cidx]
			scrabble_sum+=letter_score
		
		return scrabble_sum
	
	def generate_options(self):
		
		self.tray=self.players[self.player_idx].tray
		tray_map=self.tray.get_word_map()
		
		word=u''
		for idx in range(len(tray_map[0])):
			#print type(tray_map[0][idx])
			word+=tray_map[0][idx]
		
		fp_list=self.mkfingerprint(word)
		fp_num=self.mkfp_num(fp_list)
		
		if DEBUG:print 'tray word: ',word.encode(self.encoding)
		if DEBUG:print 'tray word fp_list=',fp_list
		if DEBUG:print 'tray word fp_num=',fp_num
		
		
		if DEBUG:print 'tws_solver: generate_options'
		gc=self.global_config
		
		if self.board.num_commited==0:		
			
			max_delta=5
			min_wc=0
			max_wc=0
			
			self.candidates=self.get_candidates(fp_list,min_wc,max_wc,max_delta)
			if len(self.candidates)==0:return None,""
			
			
			for idx in range(len(self.candidates)):
				if DEBUG:print self.candidates[idx]
				
				word=self.candidates[idx][1][0]#words
				if self.player_idx==0 and len(word)>gc['PLAYER_0_MAX_WORDLENGTH']['value']:
					if DEBUG:print 'skipping:',len(word),`word`,self.candidates[idx][1]
					continue
				
				rlist=[]
				
				if DEBUG:print 'trying candidate: ',`word`,self.candidates[idx][1]
				
				for lidx in range(len(word)):
					
					uchar=word[lidx]
					letter=self.get_unidesc_field(uchar,'VALUE')
					mod=self.get_unidesc_field(uchar,'MOD')
					if not mod:mod='NOMOD'
					gc_scoring_key=unicodedata.name(uchar)
					
					rlist.append([gc_scoring_key,int(gc['M']['value']/2),int(gc['N']['value']/2-len(word)/2+lidx)])
				
				if DEBUG:print 'score=',self.candidates[idx][5]
				self.players[self.player_idx].score+=self.candidates[idx][5]
				
				if DEBUG:print 'calling get_article: ',self.candidates[idx][1][0].encode(self.encoding)
				#last_article=self.get_article(self.candidates[idx][1][0].encode(self.encoding))
				last_article=self.get_article_via_article_lookup_key(self.candidates[idx][6][0])
				
				#2nd try with first capital
				if not last_article['key']:
					capkey=self.upper_uchar(self.candidates[idx][6][0][0])+self.candidates[idx][6][0][1:]
					last_article=self.get_article_via_article_lookup_key(capkey)
					if last_article['key']:
						if DEBUG:print 'CAPKEY SUCCESS'
					
				if not last_article['key']:
					if DEBUG:print 'received key=',last_article['key'],' continuing...'
					continue
					#msg=self.candidates[idx][6][0]+':\nNo definition available 01'
					#print `msg`
				else:	
					msg="%s: %s"%(self.candidates[idx][6][0],last_article['content'])
					#msg=self.candidates[idx][6][0]+last_article['content']
				
				#self.set_last_defn(msg)
				#if DEBUG:print 'msg=',`msg`
				
				#rval=raw_input('proceed?')
				#if rval=='q':sys.exit()
				
				if len(rlist)==0:return None,""
				return rlist,msg
			
		else:
			min_wc=1#NEED:These thresholds from config
			max_wc=1
			if self.board.num_commited==1:max_wc=1
			elif self.board.num_commited==2:max_wc=1
			elif self.board.num_commited==3:max_wc=2
			elif self.board.num_commited==4:max_wc=2
			elif self.board.num_commited==5:max_wc=3
			elif self.board.num_commited==6:max_wc=3
			else:max_wc=3
			max_delta=4
			
			self.candidates=self.get_candidates(fp_list,min_wc,max_wc,max_delta)
			
			#NEED:use WCs
			#sort words by scrabble_sum
			#do this in get_candidates() --DONE
			
			#loop over sorted words
			for idx in range(len(self.candidates)):
			  
			  self.update()
			  
			  if math.fmod(idx,100)==0:self.queue_thinking_maneuver()
			  
			  for word2fit in self.candidates[idx][1]:#loop over words with identical letter content (all with same candidate fingerprint)
				
				self.update()
				if self.STOP_RUNNING:return None,""
				
				if self.player_idx==0 and len(word2fit)>gc['PLAYER_0_MAX_WORDLENGTH']['value']:
					if DEBUG:print 'skipping:',len(word),`word`,self.candidates[idx][1]
					continue
				
				widx=self.candidates[idx][1].index(word2fit)
				
				if DEBUG:print "%d\r"%(idx),
				
				#determine WC fingerprint
				#word2fit=self.candidates[idx][1][widx]
				
				wc_list=self.candidates[idx][2]
				fp_candidate=self.mkfingerprint(word2fit)
				fp_idx_candidate=self.mkidxfingerprint(word2fit,wc_list)
				fp_wcidx_candidate=self.mkwcidxfingerprint(word2fit,wc_list)
				#print 'fp_idx_candidate=',fp_idx_candidate
				#print 'fp_wcidx_candidate=',fp_wcidx_candidate
				
				#board search for fp_wcidx_candidate
				idx_map=self.board.get_idx_map(gc['letters'])
				
				#FITROW 
				for midx in range(len(idx_map)):
					for nidx in range(0,len(idx_map[0])-len(fp_wcidx_candidate)):
						
						board_list=[]
						for fp_idx in range(0,len(fp_wcidx_candidate)):
							board_list.append(idx_map[midx][nidx+fp_idx])
							
						#print 'subtracting:',board_list,fp_wcidx_candidate
						fp_diff=self.subtract_strfp0_from_strfp1(board_list,fp_wcidx_candidate)
						if not fp_diff:continue
						#print 'fp_diff=',fp_diff
						
						all_zeros=True
						for fp_diff_idx in range(len(fp_diff)):
							if fp_diff[fp_diff_idx]!=0:all_zeros=False
							
						if all_zeros:
							
							rlist=[]
							for lidx in range(len(word2fit)):
								if board_list[lidx]=='--':
									
									uchar=word2fit[lidx]
									gc_scoring_key=unicodedata.name(uchar)
									rlist.append([gc_scoring_key,midx,nidx+lidx])
							
							#NEED:check neighborhood
							rval=self.check_row_neighborhood(midx,nidx,word2fit,fp_wcidx_candidate,idx_map)
							if not rval:continue
							
							for cidx in range(len(self.candidates)):
								if DEBUG:print self.candidates[cidx]
							
							#last_article=self.get_article(word2fit)
							last_article=self.get_article_via_article_lookup_key(self.candidates[idx][6][widx])
							
							#2nd try with first capital
							if not last_article['key']:
								capkey=self.upper_uchar(self.candidates[idx][6][0][0])+self.candidates[idx][6][0][1:]
								last_article=self.get_article_via_article_lookup_key(capkey)
								if last_article['key']:
									if DEBUG:print 'CAPKEY SUCCESS'
								
							if not last_article['key']:
								continue#11-01-2008
								#msg=self.candidates[idx][6][widx]+':\nNo definition available'
								#print `msg`
							else:
								msg="%s: %s"%(self.candidates[idx][6][widx],last_article['content'])
								#msg=self.candidates[idx][6][widx]+last_article['content']
								
							#self.set_last_defn(msg)
							if DEBUG:print 'msg=',`msg`
							
							#rval=raw_input('proceed?')
							#if rval=='q':sys.exit()
							
							if DEBUG:print 'score=',self.candidates[idx][5]
							self.players[self.player_idx].score+=self.candidates[idx][5]
							
							if len(rlist)==0:return None,""
							return rlist,msg
							
								
				#FITCOL
				for midx in range(0,len(idx_map)-len(fp_wcidx_candidate)):
					for nidx in range(len(idx_map[0])):
						
						board_list=[]
						for fp_idx in range(0,len(fp_wcidx_candidate)):
							board_list.append(idx_map[midx+fp_idx][nidx])
						
						#print 'subtracting:',board_list,fp_wcidx_candidate
						fp_diff=self.subtract_strfp0_from_strfp1(board_list,fp_wcidx_candidate)
						if not fp_diff:continue
						#print 'fp_diff=',fp_diff
						
						all_zeros=True
						for fp_diff_idx in range(len(fp_diff)):
							if fp_diff[fp_diff_idx]!=0:all_zeros=False
							
						if all_zeros:
							
							rlist=[]
							for lidx in range(len(word2fit)):
								if board_list[lidx]=='--':
										
									uchar=word2fit[lidx]
									gc_scoring_key=unicodedata.name(uchar)
									rlist.append([gc_scoring_key,midx+lidx,nidx])
							
							#NEED:check neighborhood
							rval=self.check_col_neighborhood(midx,nidx,word2fit,fp_wcidx_candidate,idx_map)
							if not rval:continue

							for cidx in range(len(self.candidates)):
								if DEBUG:print self.candidates[cidx]
							
							if DEBUG:print "%d/%d %s %d"%(idx,len(self.candidates),word2fit.encode(self.encoding),self.candidates[idx][5])
							if DEBUG:print rlist
							
							#last_article=self.get_article(word2fit)
							last_article=self.get_article_via_article_lookup_key(self.candidates[idx][6][widx])
							
							#2nd try with first capital
							if not last_article['key']:
								capkey=self.upper_uchar(self.candidates[idx][6][0][0])+self.candidates[idx][6][0][1:]
								last_article=self.get_article_via_article_lookup_key(capkey)
								if last_article['key'] and DEBUG:print 'CAPKEY SUCCESS'
							
							if not last_article['key']:
								continue#11-01-2008
								#msg=self.candidates[idx][6][widx]+':\nNo definition available'
								#print `msg`
							else:	
								msg="%s: %s"%(self.candidates[idx][6][widx],last_article['content'])
								#msg=self.candidates[idx][6][widx]+last_article['content']
							
							#self.set_last_defn(msg)
							
							#rval=raw_input('proceed?')
							#if rval=='q':sys.exit()

							if DEBUG:print 'score=',self.candidates[idx][5]
							self.players[self.player_idx].score+=self.candidates[idx][5]
							
							if len(rlist)==0:return None,""
							return rlist,msg
							
							
			return None,""


	def check_row_neighborhood(self,m,n,word,fp_wcidx_candidate,idx_map):
		rval=True
		
		#endpoints:
		if n>0:
			if idx_map[m][n-1]!='--':return False
		
		if (n+len(word))<len(idx_map[m]):
			if idx_map[m][n+len(word)]!='--':return False
		
		#check above
		if m>0:
			for nidx in range(n,n+len(word)):#-1
				if (idx_map[m-1][nidx]!='--' and fp_wcidx_candidate[nidx-n]=='--'):return False
		
		#check below
		if m<len(idx_map)-1:
			for nidx in range(n,n+len(word)):#-1
				if (idx_map[m+1][nidx]!='--' and fp_wcidx_candidate[nidx-n]=='--'):return False
		
		return rval
	
	def check_col_neighborhood(self,m,n,word,fp_wcidx_candidate,idx_map):
		rval=True
		
		#endpoints:
		if m>0:
			if idx_map[m-1][n]!='--':return False
		
		if (m+len(word))<len(idx_map):
			if idx_map[m+len(word)][n]!='--':return False
		
		#check left
		if n>0:
			for midx in range(m,m+len(word)):#-1
				if (idx_map[midx][n-1]!='--' and fp_wcidx_candidate[midx-m]=='--'):return False

		#check right
		if n<len(idx_map[0])-1:
			for midx in range(m,m+len(word)):#-1
				if (idx_map[midx][n+1]!='--' and fp_wcidx_candidate[midx-m]=='--'):return False

		return rval

	def mkidxfingerprint(self,word,wc_list):
		if DEBUG:print 'mkidxfingerprint: ',type(word),type(wc_list[0])
		if DEBUG:print `word`,`wc_list`
		letters=self.global_config['letters']
		idxfingerprint=[]
		for widx in range(len(word)):
			WC=False
			letter=word[widx]
			for wcidx in range(len(wc_list)):
				if letter==wc_list[wcidx]:WC=True
			
			if 0:pass#WC:	idxfingerprint.append("WC:%c"%letters.index(letter))
			else:idxfingerprint.append(letters.index(letter))					
		
		return idxfingerprint
							
	def mkwcidxfingerprint(self,word,wc_list):
		letters=self.global_config['letters']
		wcidxfingerprint=[]
		for widx in range(len(word)):
			WC=False
			letter=word[widx]
			for wcidx in range(len(wc_list)):
				if letter==wc_list[wcidx]:WC=True
			
			if WC:	wcidxfingerprint.append("%2d"%letters.index(letter))
			else:wcidxfingerprint.append('--')					
		
		return wcidxfingerprint

	
	def lower_uchar(self,uchar):
		
		uchar_name=None
		
		try:uchar_name=unicodedata.name(uchar)
		except Exception,e:
			
			if DEBUG:print e,type(uchar),uchar.encode(self.encoding)
			
			rval=raw_input('q?')
			if rval=='q':sys.exit()
			
			return uchar
		
		modified_uchar_name=string.replace(uchar_name,'CAPITAL','SMALL')
		modified_uchar=unicodedata.lookup(modified_uchar_name)
		return modified_uchar
	
	def upper_uchar(self,uchar):
		
		uchar_name=None
		
		try:uchar_name=unicodedata.name(uchar)
		except Exception,e:
			#print e,uchar,uchar.encode(self.encoding)
			return uchar
		
		modified_uchar_name=string.replace(uchar_name,'SMALL','CAPITAL')
		
		momdified_uchar=None
		try:
			modified_uchar=unicodedata.lookup(modified_uchar_name)
		
		except Exception,e:
			if DEBUG:print e
			return None
		
		return modified_uchar
	
	
	def get_article_via_article_lookup_key(self,article_lookup_key):
		#dh=GetArticle(article_lookup_key)
		#parser.setContentHandler(dh)
		#inf=open(os.path.join(self.env.configdir,'xdxf',self.current_resource_key,'dict.xdxf'))
		#parser.parse(inf)
		#inf.close()
		#return dh.article
		
		if self.dh.dict.has_key(article_lookup_key):
			return {'key':article_lookup_key,'content':self.dh.dict[article_lookup_key]}
		else:
			return {'key':None,'content':None}
	
	
	def get_article(self,target):
		
		#Some xdxf dicts have words all lower case, some capitalized first letter:
		#IMPORTANT: the target came from the dict, so it's there!! This func needs to retrieve SOMEHOW...
		
		cap_first=False
		
		#if 0:pass
		#elif self.current_resource_key=='German-English dictionary':cap_first=True
		#elif self.current_resource_key=='Oxford (En)':cap_first=True
		
		if cap_first==True:
			
			if DEBUG:print 'cap_first=True'
			
			mtarget=u''
			try:mtarget+=self.lower_uchar(unicode(target[0]))
			except Exception,e:
				if DEBUG:print 'fist letter...',`target[0]`,type(target[0]),type(unicode(target[0])),e,' trying again...'
				try:
					mtarget+=self.lower_uchar(target[0])
					if DEBUG:print 'okay'
				except:
					rval=raw_input('nope! capitalizing first letter failed: hit enter to return None')
					if rval=='q':sys.exit()
			
			for idx in range(1,len(target)):
				try:mtarget+=self.lower_uchar(unicode(target[idx]))
				except:
					if DEBUG:print 'get_article failes 1x: ',`target[idx]`,type(target[idx]),`mtarget`,type(target),`target`
					try:
						mtarget+=self.lower_uchar(target[idx])
					except:
						rval=raw_input('get_article failed 2x: hit enter to return None')
						if rval=='q':sys.exit()
			
			if DEBUG:print 'trying to get target article = ',mtarget.encode(self.encoding)
			
			"""
			dh=GetArticle(mtarget)
			parser.setContentHandler(dh)
			inf=open(self.current_resource_path)
			parser.parse(inf)
			inf.close()
			if dh.article['content']:return dh.article
			else:
				if DEBUG:print'failed for mtarget=',mtarget.encode(self.encoding)
			"""
			if self.dh.dict.has_key(mtarget):
				return {'key':mtarget,'content':self.dh.dict[mtarget]}
					
		
		if DEBUG:print 'using cap_first=False'
		
		mtarget=u''
		for idx in range(0,len(target)):
			try:mtarget+=self.lower_uchar(unicode(target[idx]))
			except:
				if DEBUG:print 'get_article failes 1x: ',`target[idx]`,type(target[idx]),`mtarget`,type(target),`target`
				try:
					mtarget+=self.lower_uchar(target[idx])
				except:
					rval=raw_input('get_article failed 2x: hit enter to return None')
					if rval=='q':sys.exit()
		
		if DEBUG:print 'trying to get target article = ',mtarget.encode(self.encoding)
		"""
		dh=GetArticle(mtarget)
		parser.setContentHandler(dh)
		inf=open(self.current_resource_path)
		parser.parse(inf)
		inf.close()
		return dh.article
		"""
		if self.dh.dict.has_key(mtarget):
			return {'key':mtarget,'content':self.dh.dict[mtarget]}
		else:
			return {'key':None,'content':None}	
		
		
		
	def handle_events(self):
		print 'override me'
		
	def load_config(self,intermediate_path,fname):
		print 'override me'

	def reload_configs(self):
		print 'override me'

	def on_exit(self):
		print 'override me'
				
	def mktstamp(self):
		#tstamp which increases monotonically with time
		t=time.localtime()
		YYYY="%d"%t[0]
		MM="%02d"%t[1]
		DD="%02d"%t[2]
		hh="%02d"%t[3]
		mm="%02d"%t[4]
		ss="%02d"%t[5]
		tstamp="%s%s%s%s%s%s"%(YYYY,MM,DD,hh,mm,ss)
		return tstamp

