# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getName(self):
		return "仙盟door"

	def getMainModName(self, idx):
		return "guild.guildDoor.d%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "guild.guildDoor.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from guild.guildDoor.object import cDoor as CustomDoor
'''

	def getMainContent(self, idx, data):
		dataList = []
		dataList.append("class cDoor(CustomDoor):")
		dataList.append("idx = %s" % idx)
		dataList.append("shape = %s" % data["造型"])
		dataList.append("sourceSceneId= \"%s\"" % data["场景编号"])
		dataList.append("x = %s" % data["传送点x"])
		dataList.append("y = %s" % data["传送点y"])
		dataList.append("targetSceneId= \"%s\"" % data["目标场景编号"])
		dataList.append("targetX = %s" % data["目标x"])
		dataList.append("targetY= %s" % data["目标y"])
		dataList.append("d = %s" % data["面向"])
		if hasattr(self, "customMainContent"):
			dataList.extend(self.MainContent(idx, data))
		return indent(LINE_SEP.join(dataList), 1, False)

from makeData.defines import *
