# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6419
	name = "治疗仙术"
	buffId = 918
	configInfo = {
		"生命":10,
	}
#导表结束
#群体加血，每回合给自身以外的所有队友加10%的血量

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
		self.addFunc(w, "onEndRound", self.onEndRound)
	
	def onAddWarrior(self, w):
		buff.addOrReplace(w, self.buffId, 99)
		
	def onEndRound(self, w):
		targetList = getTargetList(w)
		if not targetList:
			return

		warObj = w.war
		if hasattr(warObj.game, "getText"):
			content = warObj.game.getText(7001)
			warObj.say(w,content)
			
		warObj.rpcWarPerform(w, self.getMagId(), targetList)
		for targetW in targetList:
			hp = targetW.hpMax * self.configInfo["生命"] / 100
			targetW.addHP(hp)
		warObj.rpcWarCmdEnd(w)
			

def getTargetList(w):
	lst = []
	for targetW in w.getFriendList():
		if w is targetW:
			continue
		lst.append(targetW)

	return lst

import buff