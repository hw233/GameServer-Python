# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5152
	name = "续断"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onEndRound", recoverHp)


def recoverHp(w):
	'''回复生命
	'''
	w.addHP(w.level * 80 / 100)