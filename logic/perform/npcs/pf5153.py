# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5153
	name = "舍身"
	configInfo = {
		"伤害":lambda LV:LV*3+10,
	}
#导表结束
#死亡时，对敌方任一单位造成等级*3+10点伤害，每场战斗只会触发1次

	def onSetup(self, w):
		self.addFunc(w, "beforeDie", self.beforeDie)
		
	def beforeDie(self, vic, att):
		if hasattr(self, "hasDone"):
			return
		hp = self.transCode(self.configInfo["伤害"], vic, att)
		w = vic.getEnemyTarget()
		if w:
			w.addHP(-hp)
			self.hasDone = True
