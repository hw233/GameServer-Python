# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5118
	name = "反击"
	configInfo = {
		"概率":30,
	}
#导表结束
#受到近身伤害时，有30%的几率使用普通攻击反击对方

	def onSetup(self, w):
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		if attackType.attackType not in (ATTACK_TYPE_PHY, ATTACK_TYPE_PERFORM_PHY):
			return
		if rand(100) >= self.configInfo["概率"]:
			return
		vic.targetIdx = att.idx
		war.commands.doPhyAttack(vic, True)
	
	
from common import *
from war.defines import *
import war.commands