# -*- coding: utf-8 -*-
import makeData.pyMaker.skillSchMaker

class PyMaker(makeData.pyMaker.skillSchMaker.PyMaker):
	
	def getName(self):
		return "修炼技能"

	def getMainModName(self, idx):
		return "skill.practice.sk%s" % self.transIdx(idx)
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from skill.object import PracticeSkill as CustomSkill
'''
