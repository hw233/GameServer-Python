# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5151
	name = "冥思"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onEndRound", recoverMp)


def recoverMp(w):
	'''回复真气
	'''
	w.addMP(w.level * 30 / 100)