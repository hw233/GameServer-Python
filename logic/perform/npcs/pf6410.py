# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6410
	name = "戊土道人"
	targetType = PERFORM_TARGET_ENEMY
	targetCountMax = 1
	buffId = 917
	configInfo = {
		"特殊状态":912,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onNewRound", self.onNewRound)
		self.addFunc(w,"onEndRound", self.onEndRound)
		w.specialBuff = self.configInfo["特殊状态"]

	def onNewRound(self, w):
		if w.bout != 1:
			return
		self.autoPerform(w,1)

	def onEndRound(self, w):
		if w.bout == 1:
			return
		self.autoPerform(w,2)	

	def autoPerform(self, w, buffBout):
		'''施法
		'''
		if w.isDead():
			return
		
		warObj = w.war
		gameObj = warObj.game
		if hasattr(gameObj, "getText"):
			warObj.say(w, gameObj.getText(4016))
		
		vic = getTarget(w)
		if not vic:
			return
		warObj.rpcWarPerform(w, self.getMagId(),vic)
		if self.calHit(w,vic):
			buff.addOrReplace(vic, self.buffId, buffBout, w)
		warObj.rpcWarCmdEnd(w)

def getTarget(w):
	targetLst = w.getEnemyList()
	wr = None
	for wr in targetLst:
		if wr.isRole():
			return wr

	return wr

from common import *
import buff
