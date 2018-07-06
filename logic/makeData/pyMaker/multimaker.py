# -*- coding: utf-8 -*-
import makeData.pyMaker

class PyMaker(makeData.pyMaker.cPyMaker):
	'''多py文件生成器的基类，如任务、技能、法术等
	'''
	
	def __init__(self, *parserList):
		self.tParser = []
		self.addParser(*parserList)
	
	def transIdx(self, idx):
		'''转换编号
		'''
		return idx
	
	def getIdx(self, data):
		'''获取编号
		'''
		return int(data["编号"])

	def makeToPyFile(self):
		'''创建py文件
		'''
		modList = []
		for data in self.getParserByName("main").parseTxtTo2Dict():
			idx = self.getIdx(data)
			content = self.getMainContent(idx, data)
			if content is None:
				continue
			self.createMainPy(idx, content)
			modList.append( (idx, self.getMainModName(idx)) )
			
		self.createLoadPy(modList)
		self.updateModList(modList)
			
	def createMainPy(self, idx, content, flag=""):
		'''生成主py文件
		'''
		flagBegin = "#%s导表开始" % flag
		flagEnd = "#%s导表结束" % flag
		
		filePath = self.getMainFilePath(idx)
		if not os.path.exists(filePath):
			headContent = self.getHeadContent(idx)
			content = LINE_SEP.join([headContent, flagBegin, content, flagEnd])
		else:
			f = open(filePath, "rb")
			contentOld = f.read()
			f.close()
			idxBegin = contentOld.find(flagBegin)
			idxEnd = contentOld.find(flagEnd)
			if idxBegin == -1:
				raise Exception("错误, %s没有导表开始标志%s" % (filePath, flagBegin))
			if idxEnd == -1:
				raise Exception("错误, %s没有导表结束标志%s" % (filePath, flagEnd))
			if idxBegin > idxEnd:
				raise Exception("错误, %s导表开始/结束标志位置反了" % filePath)
			idxBegin += len(flagBegin)
			content = LINE_SEP.join([contentOld[:idxBegin], content, contentOld[idxEnd:]])

		f = open(filePath, "wb")
		try:
			f.write(content)
		finally:
			f.close()
			
	def createLoadPy(self, modList):
		'''生成加载模块
		'''
		filePath = self.getLoadFilePath()
		f = open(filePath, "rb")
		contentOld = f.read()
		f.close()
				
		importList = []
		varList = []
		for idx, mod in modList:
			importList.append("import %s" % mod)
			varList.append("moduleList[%s] = %s" % (idx, mod))
		content = LINE_SEP.join(importList) + LINE_SEP*2 + LINE_SEP.join(varList)
		
		flagBegin = "#%s导表开始" % self.getName()
		flagEnd = "#%s导表结束" % self.getName()
		idxBegin = contentOld.find(flagBegin)
		idxEnd = contentOld.find(flagEnd)
		if idxBegin == -1:
			content = LINE_SEP.join([contentOld + LINE_SEP, flagBegin, content, flagEnd])
		else:
			idxBegin += len(flagBegin)
			content = LINE_SEP.join([contentOld[:idxBegin], content, contentOld[idxEnd:]])

		f = open(filePath, "wb")
		try:
			f.write(content)
		finally:
			f.close()
			
	def updateModList(self, modList):
		'''更新模块
		'''
		for idx, mod in modList:
			hotUpdate.update(mod)
			
		loadMod = self.getLoadModName()
		if loadMod:
			hotUpdate.update(loadMod)
			
	def getMainFilePath(self, idx):
		'''主py文件路径
		'''
		modName = self.getMainModName(idx)
		modName = modName.replace(".", "/")
		return "logic/%s.py" % modName
	
	def getLoadFilePath(self):
		'''加载py文件路径
		'''
		modName = self.getLoadModName()
		modName = modName.replace(".", "/")
		return "logic/%s.py" % modName
			
	def getName(self):
		raise NotImplementedError("请在子类实现")
			
	def getMainModName(self, idx):
		'''主模块名
		'''
		raise NotImplementedError("请在子类实现")
	
	def getLoadModName(self):
		'''加载模块名
		'''
		raise NotImplementedError("请在子类实现")
	
	def getHeadContent(self, idx):
		'''文件头内容
		'''
		raise NotImplementedError("请在子类实现")
	
	def getMainContent(self, idx, data):
		'''主py内容
		'''
		raise NotImplementedError("请在子类实现")


from makeData.defines import *
import os
import hotUpdate
