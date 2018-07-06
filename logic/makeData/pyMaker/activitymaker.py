# -*- coding: utf-8 -*-
import makeData.pyMaker

class PyMaker(makeData.pyMaker.cPyMaker):
	
	def __init__(self, activityName, *parserList):
		self.activityName = activityName
		self.tParser = []
		self.addParser(*parserList)
	
	def getName(self):
		return "活动%s" % self.activityName
	
	def getMainModName(self):
		return "activity.%s" % self.activityName
	
	def getLoadModName(self):
		return "activity.load"
	
	def getMainFilePath(self):
		'''主py文件路径
		'''
		modName = self.getMainModName()
		modName = modName.replace(".", "/")
		return "logic/%s.py" % modName
	
	def getLoadFilePath(self):
		'''加载py文件路径
		'''
		modName = self.getLoadModName()
		modName = modName.replace(".", "/")
		return "logic/%s.py" % modName
	
	def makeToPyFile(self):
		'''创建py文件
		'''
		self.createMainPy(self.getMainContent())
		self.updateModList(self.getMainModName())
		
	def createMainPy(self, content, flag=""):
		'''生成主py文件
		'''
		flagBegin = "#%s导表开始" % flag
		flagEnd = "#%s导表结束" % flag
		
		filePath = self.getMainFilePath()
		if not os.path.exists(filePath):
			headContent = self.getHeadContent()
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
	
	def getHeadContent(self):
		return '''# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity
'''

	def getMainContent(self):
		dataList = []
		dataList.append("class Activity(customActivity):")
		
		for parser in self.tParser:
			dataList.append("%s%s = %s" % (LINE_SEP, parser.getVarName(), parser.getParseTxt()))

		return indent(LINE_SEP.join(dataList), 1, firstLine=False)
	
	def updateModList(self, *modList):
		'''更新模块
		'''
		for mod in modList:
			hotUpdate.update(mod)


from makeData.defines import *
import os
import hotUpdate
