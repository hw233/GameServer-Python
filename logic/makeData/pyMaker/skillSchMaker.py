# -*- coding: utf-8 -*-
import makeData.pyMaker.multimaker

class PyMaker(makeData.pyMaker.multimaker.PyMaker):
	
	def getName(self):
		return "门派技能"

	def getMainModName(self, idx):
		return "skill.school.sk%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "skill.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from skill.object import SchSkill as CustomSkill
'''
	
	def getMainContent(self, idx, data):
		dataList = []
		dataList.append("class Skill(CustomSkill):")
		dataList.append("id = %s" % idx)
		dataList.append("name = \"%s\"" % data["名称"])
		if data.get("法术"):
			dataList.append("performList = (%s,)" % data["法术"])
		if data.get("评分"):
			dataList.append("score = %s" % data["评分"])
		if data.get("技能效果"):
			applyList = transApplyList(data["技能效果"])
			dataList.append("applyList = {\n%s\n}" % applyList)
		
		if hasattr(self, "customMainContent"):
			dataList.extend(self.MainContent(idx, data))
		
		return indent(LINE_SEP.join(dataList), 1, False)

from makeData.defines import *
