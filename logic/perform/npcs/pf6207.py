# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6207
	name = "小怪自爆"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 20
	configInfo = {
		"伤害率加成":20,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onCommand", self.onCommand)
		self.addFunc(w, "onEndRound", self.onEndRound)

	def onEndRound(self, w):
		if w.hp < w.hpMax/2: #设置两回合后使用
			if not hasattr(w,"explodeBout"):
				w.explodeBout = w.bout + 3
		
	def onCommand(self, w):
		if hasattr(w,"explodeBout") and w.bout == w.explodeBout:
			war.commands.setCommand_Mag(w.war, w, performId=self.id)
			return

		if w.targetPerformId == self.id:
			war.commands.setCommand(w.war, w, CMD_TYPE_PHY)

	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		damageRatio = self.configInfo["伤害率加成"]
		att.war.rpcWarPerform(att, self.getMagId(), targetList)
		for wr in targetList:
			wr.addHP(-wr.hpMax * damageRatio/100)

	def afterPerform(self, att, vicCast):
		att.war.kickWarrior(att)
		CustomPerform.afterPerform(self, att, vicCast)

from common import *
from war.defines import *
import war.commands