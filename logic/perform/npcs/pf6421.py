# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6421
	name = "妖莲幻术"
	bout = 2
	buffId = 920
	configInfo = {
		"目标buff":922,
	}
#导表结束
#每回合固定全封1个队员，不可解除，如果没有队员，则封印异兽

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
		self.addFunc(w, "onEndRound", self.onEndRound)
	
	def onAddWarrior(self, w):
		buff.addOrReplace(w, self.buffId, 99)
		
	def onEndRound(self, w):
		targetList = []
		buffId = self.configInfo["目标buff"]
		for targetW in w.getEnemyList():
			if not (targetW.isRole() or targetW.isPet() or targetW.isBuddy()):
				continue
			if buff.has(targetW, buffId):
				continue
			targetList.append(targetW)
		
		if not targetList:
			return
		
		warObj = w.war
		if hasattr(warObj.game, "getText"):
			content = warObj.game.getText(7003)
			warObj.say(w,content)

		targetList.sort(key=lambda targetW: 1 if targetW.isPet() else 0)
		targetW = targetList[0]
		warObj.rpcWarPerform(w, self.getMagId(), targetW)
		bout = self.calBout(w, targetW, buffId)
		buff.addOrReplace(targetW, buffId, bout, w)
		warObj.rpcWarCmdEnd(w)
		

import buff