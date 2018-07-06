# -*- coding: utf-8 -*-
import makeData.pyMaker.skillSchMaker

class PyMaker(makeData.pyMaker.skillSchMaker.PyMaker):
	
	def getName(self):
		return "特技特效"

	def getMainModName(self, idx):
		return "skill.equip.sk%s" % self.transIdx(idx)
	
	def getLoadModName(self):
		return "skill.load"
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from skill.object import EquipSkill as CustomSkill
'''

