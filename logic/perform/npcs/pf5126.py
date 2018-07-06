# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5126
	name = "化生"
	configInfo = {
		"生命":12,
		"上限":lambda LV:LV*6,
	}
#导表结束
#非第一回合进入战场时，回复主人12%的生命值，最大不超过其等级*6

	def onSetup(self, w):
		self.addFunc(w, "onSummoned", self.onSummoned)
		
	def onSummoned(self, att, vic):
		hp = att.hp * self.configInfo["生命"] / 100
		hpLimit = self.transCode(self.configInfo["上限"], vic, att)
		hp = min(hp, hpLimit)
		att.addHP(hp, vic)
		