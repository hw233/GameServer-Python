# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5306
	name = "龙卷蛇盘"
	configInfo = {
		"反击概率":50,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		if att.isDead() or vic.isDead():
			return
		if attackType.attackType not in (ATTACK_TYPE_PHY, ATTACK_TYPE_PERFORM_PHY):
			return
		if rand(100) < self.configInfo["反击概率"]:
			vic.targetIdx = att.idx
			war.commands.doPhyAttack(vic, True)

from common import *
from war.defines import *
import war.commands