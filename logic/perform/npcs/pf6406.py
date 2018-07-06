# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6406
	name = "金臂行者"
	buffId = 915
	configInfo = {
		"特殊状态":908,
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
		'''自动施法
		'''
		if w.isDead():
			return
		
		warObj = w.war
		gameObj = warObj.game
		if hasattr(gameObj, "getText"):
			warObj.say(w, gameObj.getText(4012))
			
		warObj.rpcWarPerform(w, self.getMagId(),w)
		bfObj = buff.addOrReplace(w, self.buffId, 2, w)
		warObj.rpcWarCmdEnd(w)

from common import *
import buff
