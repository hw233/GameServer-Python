# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6412
	name = "沧浪羽士"
	configInfo = {
		"特殊状态":914,
		"回复加成":30,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onNewRound", self.onNewRound)
		self.addFunc(w,"onEndRound", self.onEndRound)
		w.specialBuff = self.configInfo["特殊状态"]

	def onNewRound(self, w):
		if w.bout != 1:
			return
		self.autoPerform(w)

	def onEndRound(self, w):
		if w.bout == 1:
			return
		self.autoPerform(w)	

	def autoPerform(self, w):
		'''自动治疗
		'''
		if w.isDead():
			return
		targetList = getTargetList(w)
		if not targetList:
			return
		
		warObj = w.war
		gameObj = warObj.game
		if hasattr(gameObj, "getText"):
			warObj.say(w, gameObj.getText(4014))

		warObj.rpcWarPerform(w, self.getMagId(), targetList)
		for monsterW in targetList:
			if monsterW.monsterType != MONSTER_TYPE_NORMAL:
				continue
			monsterW.addHP(monsterW.hpMax * self.configInfo["回复加成"]/ 100)

		warObj.rpcWarCmdEnd(w)

def getTargetList(w):
	targetList = []
	for w in w.getFriendList():
		if w.hp < w.hpMax:
			targetList.append(w)

	return targetList

from common import *
from war.defines import *
import war.warctrl
import buff