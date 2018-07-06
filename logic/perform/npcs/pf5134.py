# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5134
	name = "震慑"
	bout = 2
	buffId = 224
	configInfo = {
		"概率":lambda LV,mag:(mag-10)/(LV+1),
	}
#导表结束
#造成法术伤害时，有(法力点数-10)/等级*1%的几率使目标下回合被迫执行防御，群攻技能只对主目标有效

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if attackType.attackType != ATTACK_TYPE_PERFORM_MAG:
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