# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6407
	name = "桑木仙姥"
	configInfo = {
		"特殊状态":909,
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
		'''施法
		'''
		if w.isDead():
			return
		
		warObj = w.war
		gameObj = warObj.game
		if hasattr(gameObj, "getText"):
			warObj.say(w, gameObj.getText(4013))

		count = getCount(w)
		if not count or not hasattr(warObj,"summonMonsterObj"):
			return
		warObj.rpcWarPerform(w, self.getMagId())
		for i in xrange(count):
			monsterW = warObj.addMonsterFight(warObj.summonMonsterObj, TEAM_SIDE_2)
			warObj.rpcAddWarrior(monsterW, None, True)
			warObj.rpcWarAllBuff(monsterW)
			warObj.setDefaultCommand(monsterW)
			monsterW.isAct = False
		warObj.rpcWarCmdEnd(w)

def getCount(w):
	if w.hp >= w.hpMax / 2:
		count = 1
	else:
		count = 2

	countMax = 10 - getNormalMonsterCount(w)
	return min(countMax,count)

def getNormalMonsterCount(w):
	count = 0
	for wr in w.war.teamList[TEAM_SIDE_2].itervalues():
		if wr.type == WARRIOR_TYPE_NORMAL:
			count += 1
	return count


from common import *
from war.defines import *
import war.warctrl
import buff