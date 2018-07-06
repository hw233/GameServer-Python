# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6417
	name = "恒山君分身"
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onEndRound", self.onEndRound)

	def onEndRound(self, w):
		warObj = w.war
		for wr in warObj.teamList[w.side].values():
			if wr.performListPassive.get(self.id):
				continue
			warObj.kickWarrior(wr)

		self.summonMoster(warObj,w)

	def summonMoster(self, warObj, w):
		if not hasattr(warObj,"summonMonsterList"):
			return
		# if warObj.game:
		# 	content = warObj.game.getText(3006)
		# 	warObj.say(w,content,2)
		warObj.rpcWarPerform(w, self.getMagId())
		pos = rand(len(warObj.summonMonsterList)-1)
		targetW = None
		for idx,monsterObj in enumerate(warObj.summonMonsterList):
			monsterW = warObj.addMonsterFight(monsterObj, w.side)
			warObj.rpcAddWarrior(monsterW, None, True)
			warObj.rpcWarAllBuff(monsterW)
			warObj.setDefaultCommand(monsterW)
			monsterW.isAct = False
			if idx == pos:
				targetW = monsterW
				
		warObj.rpcWarCmdEnd(w)
		if targetW:
			w.war.exchangePos(w, targetW)

from common import *
from war.defines import *
import war