# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3206
	name = "浩然气"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onRevive", self.onRevive)

	def onRevive(self, vic ,att):
		'''回复生命
		'''
		if hasattr(self, "hasDone"):
			return
		vic.addHP(1)
		self.hasDone = True


from common import *