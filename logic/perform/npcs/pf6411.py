# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6411
	name = "天罗子"
	buffId = 923
	configInfo = {
		"特殊状态":913,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w,"onNewRound", self.onNewRound)
		self.addFunc(w,"onEndRound", self.onEndRound)
		w.specialBuff = self.configInfo["特殊状态"]

	def onEndRound(self, w):
		if hasattr(w.war,"firstDieBout"):
			return
		wr = getDeadTarget(w)
		if not wr:
			return

		w.war.firstDieBout = w.bout
		bfObj = buff.addOrReplace(w, self.buffId, 10, w)

	def onNewRound(self, w):
		'''施法
		'''
		if not hasattr(w.war,"firstDieBout"):
			return

		if (w.bout - w.war.firstDieBout) % 10 == 8:
			w.war.game.say(w,4034)
		elif (w.bout - w.war.firstDieBout) % 10 == 0:
			bfObj = buff.addOrReplace(w, self.buffId, 10, w)
			target = getDeadTarget(w)
			if not target:
				return
			w.war.rpcWarPerform(w, self.getMagId(),target)
			target.addHP(target.hpMax)
			w.war.rpcWarCmdEnd(w)

def getDeadTarget(w):

	for wr in w.war.teamList[TEAM_SIDE_2].itervalues():
		if wr.isDead():
			return wr

	return None

from common import *
from war.defines import *
import buff