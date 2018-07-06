# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5141
	name = "妙法"
	configInfo = {
		"概率":10,
		"符能":5,
	}
#导表结束
#使用法术攻击时，有10%的几率为主人增加5点符能
	def onSetup(self, w):
		if not w.isPet():
			return
		self.addFunc(w, "onPerform", self.onPerform)
		
	def onPerform(self, att, vicCast, attackType):
		if attackType.attackType != ATTACK_TYPE_PERFORM_MAG:
			return
		if rand(100) >= self.configInfo["概率"]:
			return

		fuWen = self.configInfo["符能"]
		roleW = att.war.getWarrior(att.ownerIdx)
		if roleW and not roleW.isDead():
			roleW.addFuWen(fuWen)

from common import *
from war.defines import *