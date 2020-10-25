import sys
import xml.sax
import xml.parsers.expat
import time 
import pickle
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import re
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
import string
import os
import time
import math
import operator

root_path=sys.argv[1]
fo1= open(str(root_path),"r")
sec=[]

fsec=open('/split_index/sec_ind.txt',"r")
line=fsec.readline()
sec = line.strip('][').split(', ')
fsec.close()
fw1=open("queries_op.txt","w")

fsec=open('/split_index/tc.txt',"r")
l=fsec.readline()
tc=int(l)


def which_file(wrd):
  val=len(sec)-1
  for i in range(0,len(sec)-1):
    if wrd >= sec[i] and wrd < sec[i+1]:
      val=i
      break
  return val


def rpl(w):
  val=which_file(w)
  file = open('/split_index/'+str(val)+'.txt', 'r')
  pl=p(w,file)
  file.close()
  pl=pl[:-1]
  pl=pl.split(":")[1]
  pl=pl.split(",")
  return pl

def query_parse(q):
  flag=0
  if ":" not in q:
    flag=1
    k,qq=q.split(",")
    q1=qq.split()
    return k,flag,q1
  k,q=q.split(",")
  q=q.lower().split(":")
  # print(q)
  q1=[]
  if(len(q)==2):
    q1.append(q[0]+":"+q[1])
  else:
    q1.append(q[0]+":"+q[1][:-2])
  for i in range(1,len(q)-1):
    s=""
    if(i+1==len(q)-1):
      s+=q[i][-1]+":"+q[i+1]
    else:
      s+=q[i][-1]+":"+q[i+1][:-2]
    q1.append(s)
  return k,flag,q1

def getList(dict): 
    list = [] 
    for key in dict.keys(): 
        list.append(int(key)) 
    return list


qline=fo1.readline()
qline=qline.strip()
while qline:
	s11=time.time()
    k,flag,q1=query_parse(qline)
    tfidf=defaultdict(float)
    field=["t","c","i","l","r","b"]
    if flag==1:
		for query in q1:
	    	pl=rpl(query)
		    N1={}
		    N=[]
		    N2={}
		    for w in pl:
		      s=""
		      for i in w:
		        if i.isalpha():
		          if s not in N:
		            N.append(s)
		            N1[s]=[]
		            N2[s]=0
		        else:
		          s+=i
	    	for doc in pl:
	      		for f in field:
	        		if f in doc:
	          			d,c=doc.split(f)
	          			N2[str(d)] += int(c)
	          			if f=="t":
	            			N2[str(d)] += int(c)*2000
	          			# if f=="i":
	            			# N2[str(d)] +=int(c)*2
		    term_tfidf={}
		    d={}
		    idf=math.log2(tc/len(N))
		    for i in N2:
		      term_tfidf[i]=idf*math.log1p(N2[i])
		      tfidf[i] += term_tfidf[i]
		    # term_tfidf = dict(sorted(term_tfidf.items(), key=operator.itemgetter(1),reverse=True))
		    # print(term_tfidf)
	  	tfidf = dict(sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True))
	  	# print(tfidf)
	elif flag==0:
  		for q in q1:
		    f,query=q.split(":")
		    pl=rpl(query)
		    print(query,pl)
		    N=[]
		    N1={}
		    N2={}
		    for w in pl:
		     	s=""
		      	for i in w:
		        	if i.isalpha():
		          		if s not in N:
		            		N.append(s)
		            		N1[s]=[]
		            		N2[s]=0
        			else:
          				s+=i
    		for doc in pl:
      			if f in doc:
        			d,c=doc.split(f)
        			N2[str(d)] += int(c)
        			if f=="t":
          				N2[str(d)] += int(c)*2000
        			# if f=="i":
          				# N2[str(d)] +=int(c)*2
		    term_tfidf={}
		    d={}
		    idf=math.log2(tc/len(N))
		    for i in N2:
		    	term_tfidf[i]=idf*math.log1p(N2[i])
		    	tfidf[i] += term_tfidf[i]
		    # term_tfidf = dict(sorted(term_tfidf.items(), key=operator.itemgetter(1),reverse=True))
		    # print(term_tfidf)
		tfidf = dict(sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True))
  # print(tfidf)
	k_title=getList(tfidf)
	e11=time.time()
	for i in range(int(k)):
		x=int(k_title[i])
		# print(x,title_array[x-1])
		fw1.write(str(x)+", "+str(title_array[x-1]))
	fw1.write(str(e11-s11),+", "+str((e11-s11)/k))
fw1.close()
fo1.close()
	