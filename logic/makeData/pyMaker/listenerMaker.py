# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getName(self):
		return ""

	def getMainModName(self, idx):
		return "listener.l%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "listener.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener
'''

	def getMainContent(self, idx, data):
		eventTypeList = self.transEventTypeList(data.get("监听事件类型"))
		conditionList = self.transConditionList(data.get("触发条件"))
		conditionScope = self.transConditionScope(data.get("条件范围"))
		eventList = self.transEventList(data.get("触发事件"))

		dataList = []
		dataList.append("class Listener(CustomListener):")
		dataList.append("eventTypeList = (%s)" % eventTypeList)
		dataList.append("conditionList = (\n%s\n)" % conditionList)
		dataList.append("conditionScope = \"%s\"" % conditionScope)
		dataList.append("eventList = (\n%s\n)" % eventList)
		return indent(LINE_SEP.join(dataList), 1, False)
	
	def transEventTypeList(self, s):
		if not s:
			return ""

		lst = []
		for eventTypeStr in s.split(","):
			lst.append("\"%s\"," % eventTypeStr)
		return "".join(lst)
	
	def transConditionList(self, s):
		if not s:
			return ""
		
		for k,v in operatorList:
			s = s.replace(k, v)
		
		lst = []
		for conStr in s.split("||"):
			idx, con = conStr.split(":")
			lst.append("(%s,\"%s\")," % (idx, con))
		return indent(LINE_SEP.join(lst), 1)
	
	def transConditionScope(self, s):
		if not s:
			return ""
		s = s.replace("&", " and ")
		s = s.replace("|", " or ")
		return s
	
	def transEventList(self, s):
		if not s:
			return ""
		
		lst = []
		for eventStr in s.split("||"):
			lst.append("\"%s\"," % eventStr)
		return indent(LINE_SEP.join(lst), 1)


operatorList = (
	("=", "=="),
	("≤", "<="),
	("≥", ">="),
	("<>", "!="),
)

from makeData.defines import *
import makeData.txtParser
import buff.defines
