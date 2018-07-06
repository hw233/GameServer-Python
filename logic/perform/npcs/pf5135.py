# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5135
	name = "眩晕"
	bout = 1
	buffId = 225
	configInfo = {
		"概率":lambda LV,str:(str-10)/(LV+1),
	}
#导表结束
#造成物理伤害时，有(力量点数-10)/等级*1%的几率令敌方陷入眩晕状态导致本回合不能出手，群攻技能只对主目标有效

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if attackType.attackType not in phyAttackTypeList:
			return
		if vic.attackedIdx != 0:
			return
		if vic.hasApply("坚韧") or vic.hasApply("高级坚韧"):
			return
		if rand(100) >= self.transCode(self.configInfo["概率"], att, vic):
			return
		
		bout = self.calBout(att, vic, self.buffId)
		buff.addOrReplace(vic, self.buffId, bout, att)
		

from common import *
from war.defines import *
import buff