# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5252
	name = "高级续断"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onEndRound", recoverHp)


def recoverHp(w):
	'''回复生命
	'''
	w.addHP(w.level * 150 / 100)