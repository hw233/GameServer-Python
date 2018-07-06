# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6413
	name = "百分比扣血"
	configInfo = {
		"伤害率加成":5,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onNewRound", self.onNewRound)


	def onNewRound(self, w):
		'''扣血
		'''
		damageRatio = self.configInfo["伤害率加成"]
		targetList = w.getEnemyList()

		# w.war.rpcWarPerform(w, self.getMagId(), targetList)
		for wr in targetList:
			wr.addHP(-wr.hpMax * damageRatio/100)
		# w.war.rpcWarCmdEnd(w)

from common import *