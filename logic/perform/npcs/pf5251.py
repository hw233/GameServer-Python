# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5251
	name = "高级冥思"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onEndRound", recoverMp)


def recoverMp(w):
	'''回复真气
	'''
	w.addMP(w.level * 50 / 100)