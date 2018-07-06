# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3204
	name = "流霜"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onEndRound", recoverHp)


def recoverHp(w):
	'''回复生命
	'''
	if w.isDead():
		return
	w.addHP(w.level * 120 / 100)