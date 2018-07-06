# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5617
	name = "缘起缘灭"
	configInfo = {
		"生命":15,
		"次数上限":3,
	}
#导表结束
#阵亡时，为己方所有单位回复生命上限15%的生命，每场战斗最多3次

	def onSetup(self, w):
		self.times = 0
		self.addFunc(w, "beforeDie", self.beforeDie)
		
	def beforeDie(self, vic, att):
		self.times += 1
		if self.times > self.configInfo["次数上限"]:
			return

		for w in vic.getFriendList():
			if w is vic:
				continue
			hp = w.hpMax * self.configInfo["生命"] / 100
			w.addHP(hp, vic)