# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6420
	name = "百毒真经"
	buffId = 919
	configInfo = {
		"生命":10,
	}
#导表结束
#每回合在进入战斗前给对方所有成员扣除当前10%的血量

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
		self.addFunc(w, "onEndRound", self.onEndRound)
	
	def onAddWarrior(self, w):
		buff.addOrReplace(w, self.buffId, 99)
		
	def onEndRound(self, w):
		warObj = w.war
		if hasattr(warObj.game, "warObj"):
			content = warObj.game.getText(7002)
			warObj.say(w,content)

		targetList = w.getEnemyList()
		warObj.rpcWarPerform(w, self.getMagId(), targetList)
		for targetW in targetList:
			hp = targetW.hp * self.configInfo["生命"] / 100
			targetW.addHP(-hp)
		warObj.rpcWarCmdEnd(w)

import buff