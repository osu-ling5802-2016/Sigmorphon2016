#!/usr/bin/python
# -*- coding: latin-1 -*-

from math import *
import sys
import re
import operator
import codecs


prefix=""
suffix=""
lang=input("Enter language:")
task=input("enter task:")

currentfile=codecs.open(lang+"-task1-"+task+".txt",encoding='utf-8')
outputfile1=codecs.open(task+"CRF_"+lang+".txt",mode='w',encoding='utf-8')


variabledict={}
for line in currentfile:
	wrds=line.split()
	wrds1=re.split(' |,|\t|\n|=',wrds[1])
	for j in range(0,len(wrds1),2):
		variabledict[wrds1[j]]=0
		
print variabledict
	
linenum=0
currentfile=codecs.open(lang+"-task1-"+task+".txt",encoding='utf-8')

for line in currentfile:
	wrds=line.split()
	wrds1=re.split(' |,|\t|\n|=',wrds[1])
	wrds=wrds[0]
	
	#outputfile1.write("_ ")
	#for variable,value in variabledict.iteritems():
	#	try:
	#		l=wrds1.index(variable)
	#		outputfile1.write(wrds1[l+1]+" ")
	#	except ValueError:
	#		outputfile1.write("None ")
	#outputfile1.write("\n")		
	for i in range(len(wrds)):
		outputfile1.write(wrds[i]+" ")
		for variable,value in variabledict.iteritems():
			try:
				l=wrds1.index(variable)
				outputfile1.write(wrds1[l+1]+" ")
			except ValueError:
				outputfile1.write("None ")
		outputfile1.write("\n")
	outputfile1.write("_ ")
	for variable,value in variabledict.iteritems():
		try:
			l=wrds1.index(variable)
			outputfile1.write(wrds1[l+1]+" ")
		except ValueError:
			outputfile1.write("None ")
	outputfile1.write("\n")
	outputfile1.write("\n")
	linenum=linenum+1
	if(linenum>1000):
		sys.exit(0)
	print linenum
	
	
	
