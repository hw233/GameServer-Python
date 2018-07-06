# -*- coding: utf-8 -*-
import makeData.pyMaker.skillSchMaker

class PyMaker(makeData.pyMaker.skillSchMaker.PyMaker):
	
	def getName(self):
		return "帮派技能"

	def getMainModName(self, idx):
		return "skill.guilds.sk%s" % self.transIdx(idx)
	
	def getHeadContent(self, idx):
		return '''# -*- coding: utf-8 -*-
from skill.object import GuildSkill as CustomSkill
'''


from makeData.defines import *