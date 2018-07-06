# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3202
	name = "生死意"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onRevive", onRevive)


def onRevive(w ,att):
	'''回复生命
	'''
	if rand(100) < 15:
		w.addHP(w.hpMax*15/100)


from common import *