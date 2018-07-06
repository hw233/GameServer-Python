#!/bin/env python
# -*- coding: utf-8 -*-



class cNode(object):
	def __init__(self):
		self.children = None
		
# The encode of word is UTF-8
# The encode of message is UTF-8
class cDfa(object):
	def __init__(self,lWords):
		self.root=None
		self.root=cNode()
		for sWord in lWords:
			self.addWord(sWord)

	# The encode of word is UTF-8
	def addWord(self,word):
		node = self.root
		iEnd=len(word)-1
		for i in xrange(len(word)):
			if node.children == None:
				node.children = {}
				if i!=iEnd:
					node.children[word[i]]=(cNode(),False)
				else:
					node.children[word[i]]=(cNode(),True)

			elif word[i] not in node.children:
				if i!=iEnd:
					node.children[word[i]]=(cNode(),False)
				else:
					node.children[word[i]]=(cNode(),True)
			else: #word[i] in node.children:
				if i==iEnd:
					Next,bWord=node.children[word[i]]
					node.children[word[i]]=(Next,True)

			node=node.children[word[i]][0]

	def isContain(self,sMsg):
		uMsg = sMsg.decode('utf-8')
		root=self.root
		iLen=len(uMsg)
		for i in xrange(iLen):
			p = root
			j = i
			while (j<iLen and p.children!=None and uMsg[j] in p.children):
				(p,bWord) = p.children[uMsg[j]]
				if bWord:
					return True
				j = j + 1
		return False

	def filter(self,sMsg):
		sMsg = sMsg.decode('utf-8')
		lNew=[]
		root=self.root
		iLen=len(sMsg)
		i=0
		bContinue=False
		while i<iLen:
			p=root
			j=i
			while (j<iLen and p.children!=None and sMsg[j] in p.children):
				(p,bWord) = p.children[sMsg[j]]
				if bWord:
					#print sMsg[i:j+1]
					lNew.append(u'*'*(j-i+1))#关键字替换
					i=j+1
					bContinue=True
					break
				j=j+1
			if bContinue:
				bContinue=False
				continue
			lNew.append(sMsg[i])
			i=i+1
		return ''.join(lNew)



import time
import sys
import keywords

if 'glKeyWord' not in globals():
	glKeyWord=[]
	for w in keywords.gtDeny:
		glKeyWord.append(w.decode('utf-8'))

	gDfa = cDfa(glKeyWord)