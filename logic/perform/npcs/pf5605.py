# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5605
	name = "天道莫名"
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onRevive", self.onRevive)
		
	def onRevive(self, vic, att):
		if rand(100) >= 20:
			return

# 		vic.war.printDebugMsg("\t\t[%s]身上法术[%s]的复活效果生效了" % (vic.name, self.name))
		hp = vic.getHPMax() * 20 / 100
		vic.addHP(hp, vic)
		self.performSay(vic)
		
from common import *