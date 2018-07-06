# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getName(self):
		return "仙盟npc"

	def getMainModName(self, idx):
		return "guild.guildNpc.n%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "guild.guildNpc.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from guild.object import Npc as CustomNpc
'''
	
	def getMainContent(self, idx, data):
		dataList = []
		dataList.append("class Npc(CustomNpc):")
		dataList.append("idx = %s" % idx)
		dataList.append("name = \"%s\"" % data["名称"])
		dataList.append("typeName = \"%s\"" % data["类型"])
		dataList.append("pos = (%s)" % data["坐标"])
		
		if data.get("造型"):
			shape, shapeParts = template.transShapeStr(data["造型"])
			dataList.append("shape = %s" % shape)
			dataList.append("shapeParts = %s" % shapeParts)
		if data.get("染色"):
			colors = template.transColorsStr(data["染色"])
			dataList.append("colors = %s" % colors)
		if data.get("称谓"):
			dataList.append("title = '''%s'''" % data["称谓"])
		if data.get("对白编号"):
			dataList.append("chatList = (%s,)" % data["对白编号"])
		
		if hasattr(self, "customMainContent"):
			dataList.extend(self.MainContent(idx, data))
		
		return indent(LINE_SEP.join(dataList), 1, False)

from makeData.defines import *
import template