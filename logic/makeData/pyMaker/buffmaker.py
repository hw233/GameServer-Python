# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getName(self):
		return ""

	def getMainModName(self, idx):
		return "buff.bf%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "buff.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff
'''
	
	def getMainContent(self, idx, data):
		name = data["名称"]
		buffType = buff.defines.getBuffTypeDesc(data["类型"])
		
		dataList = []
		dataList.append("class Buff(CustomBuff):")
		dataList.append("name = \"%s\"" % name)
		dataList.append("type = %s" % buffType)
		if data.get("效果"):
			applyList = transApplyList(data["效果"])
			dataList.append("applyList = {\n%s\n}" % applyList)
		if data.get("不可解除"):
			dataList.append("removable = False")
		if data.get("不可叠加"):
			dataList.append("replacable = False")
		return indent(LINE_SEP.join(dataList), 1, False)


from makeData.defines import *
import buff.defines
