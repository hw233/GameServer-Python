# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5304
	name = "无冬之眠"
	configInfo = {
		"回合":3,
		"生命值":20,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onNewRound", self.onNewRound)
		
	def onNewRound(self, w):
		if w.bout % self.configInfo["回合"] != 0:
			return

		w.setBoutApply("禁止指令", True)
		hp = w.hpMax * self.configInfo["生命值"] / 100
		w.addHP(hp, w)