# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6409
	name = "赤霞神君"
	targetType = PERFORM_TARGET_FRIEND
	targetCountMax = 1
	buffId = 916
	configInfo = {
		"特殊状态":911,
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
			warObj.say(w, gameObj.getText(4015))
		
		vic = w.getFriendTarget()
		w.war.rpcWarPerform(w, self.getMagId(),vic)
		bfObj = buff.addOrReplace(vic, self.buffId, 2, w)
		w.war.rpcWarCmdEnd(w)

from common import *
from war.defines import *
import war.warctrl
import buff