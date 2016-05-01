#!/usr/bin/python
# -*- coding: latin-1 -*-

from math import *
import sys
import re
import operator
import codecs
import random


'''
Example:
Enter language:"turkish"
enter task:"train"


Outputs:trainCRF_turkish.txt
trainCRF_turkish_labels.txt
'''
prefix=""
suffix=""
lang=input("Enter language:")
task=input("enter task:")

currentfile=codecs.open(lang+"-task1-"+task+"-rules-3.txt",encoding='utf-8')
outputfile1=codecs.open(task+"CRF_"+lang+".txt",mode='w',encoding='utf-8')


variabledict={}
for line in currentfile:
	wrds=line.split()
	wrds1=re.split(' |,|\t|\n|=',wrds[1])
	for j in range(0,len(wrds1),2):
		variabledict[wrds1[j]]=0
		
print variabledict
	
linenum=0
currentfile=codecs.open(lang+"-task1-"+task+"-rules-3.txt",encoding='utf-8')
randomlist=[] 
for i in range(3500):
	randomlist.append(random.randint(1, 12336))
	
for line in currentfile:
	linenum=linenum+1
	if linenum not in randomlist:
		continue
	print linenum
	wrds=line.split()
	wrds1=re.split(' |,|\t|\n|=',wrds[1])
	wrds=re.split(';',wrds[-1])
	
	if(wrds[0] == "None"):
		continue
		
	for i in range(len(wrds)):
		k=wrds[i].index(',')
		outputfile1.write(wrds[i][1:k]+" ")
		for variable,value in variabledict.iteritems():
			try:
				l=wrds1.index(variable)
				outputfile1.write(wrds1[l+1]+" ")
			except ValueError:
				outputfile1.write("None ")
		outputfile1.write(" "+wrds[i][k+1:len(wrds[i])-1]+"\n")
		
	outputfile1.write("\n")
	
	
	
	
