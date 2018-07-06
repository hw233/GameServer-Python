# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getName(self):
		return "状态配置"

	def getMainModName(self, idx):
		return "state.st%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "state.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from state.object import State as customState
'''
	
	def getMainContent(self, idx, data):
		no = data["编号"]
		name = data["名称"]
		info = data["信息"]
		dataList = []
		dataList.append("class State(customState):")
		dataList.append("no= %s" % no)
		dataList.append("name = \"%s\"" % name)
		dataList.append("info = \"%s\"" % info)
		return indent(LINE_SEP.join(dataList), 1, False)

from makeData.defines import *