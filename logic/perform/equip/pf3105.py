# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3105
	name = "风鸣"
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onEndRound", recoverFuwen)


def recoverFuwen(w):
	'''回复符能
	'''
	if w.bout % 2 != 1 or w.fuwen>20:
		return
	w.addFuWen(2)