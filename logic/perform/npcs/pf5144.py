# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5144
	name = "汇灵"
	configInfo = {
		"符能":20,
	}
#导表结束

	def onSetup(self, w):
		if not w.isPet():
			return
		self.addFunc(w, "beforeDie", self.beforeDie)
		
	def beforeDie(self, vic, att):
		roleW = vic.war.getWarrior(vic.ownerIdx)
		if roleW and not roleW.isDead():
			roleW.addFuWen(self.configInfo["符能"])