# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getIdx(self, data):
		return int(data["成就编号"])
	
	def getName(self):
		return ""

	def getMainModName(self, idx):
		return "achv.a%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "achv.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement
'''

	def getMainContent(self, idx, data):
		dataList = []
		dataList.append("class Achievement(CustomAchievement):")
		if data.get("类型"):
			kind = self.transKind(data["类型"])
			dataList.append("kind = %s" % kind)
		dataList.append("id = %s" % data["成就编号"])
		dataList.append("name = \"%s\"" % data["成就名称"])
		dataList.append("point = %s" % data["成就点"])
		if isValidStr(data.get("隐藏")):
			dataList.append("hidden = True")
		if isValidStr(data.get("总进度")):
			dataList.append("totalProgress = %s" % data["总进度"])
		if isValidStr(data.get("条件列表")):
			conditionList = self.transConditionList(data["条件列表"])
			dataList.append("conditionList = {\n%s\n}" % conditionList)
		if isValidStr(data.get("事件列表")):
			eventList = self.transEventList(data["事件列表"])
			dataList.append("eventList = (\n%s\n)" % eventList)
		if isValidStr(data.get("时间限制")):
			dataList.append("timeLimit = %s" % data["时间限制"])
		
		return indent(LINE_SEP.join(dataList), 1, False)
	
	def transKind(self, kindName):
		if kindName not in achvKindDesc:
			raise Exception("非法的成就类型，请检查类型:%s" % kindName)
		return achvKindDesc[kindName]
	
	def transEventList(self, s):
		if not s:
			return ""
		
		lst = []
		for eventStr in s.split("||"):
			lst.append("\"%s\"," % eventStr)
		return indent(LINE_SEP.join(lst), 1)
	
	def transConditionList(self, s):
		if not s:
			return ""

		conditionList = []
		for idx, condVal in enumerate(s.split(",")):
			condNo = idx + 1
			conditionList.append("%s:%s," % (condNo, condVal))
		return indent(LINE_SEP.join(conditionList), 1)
			

from makeData.defines import *
import makeData.txtParser
from achv.defines import *
