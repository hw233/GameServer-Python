# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5143
	name = "怒火"
	configInfo = {
		"愤怒":15,
	}
#导表结束
#异兽死亡出场时，增加主人15点愤怒

	def onSetup(self, w):
		if not w.isPet():
			return
		self.addFunc(w, "beforeDie", self.beforeDie)
		
	def beforeDie(self, vic, att):
		roleW = vic.war.getWarrior(vic.ownerIdx)
		if roleW and not roleW.isDead():
			roleW.addSP(self.configInfo["愤怒"])