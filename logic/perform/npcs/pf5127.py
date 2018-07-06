# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5127
	name = "唤灵"
	configInfo = {
		"符能":15,
	}
#导表结束
#非第一回合进入战场时，回复主人15点的符能

	def onSetup(self, w):
		self.addFunc(w, "onSummoned", self.onSummoned)
		
	def onSummoned(self, att, vic):
		fuWen = self.transCode(self.configInfo["符能"], vic, att)
		att.addFuWen(fuWen)
		