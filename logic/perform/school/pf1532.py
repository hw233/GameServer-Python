# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1532
	name = "祸水滔天"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,SLV:SLV/35+3
	targetCountMax = 5
	bout = lambda self,LV,SLV:(SLV-LV+2)/10+4
	boutMax = 4
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+30,
		"符能": 25,
	}
	buffId = 116
	speRatio = 107
	configInfo = {
		"伤害率":(30,25),
	}
#导表结束

	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		CustomPerform.afterAttack(self, att, vic, vicCast, dp, targetCount)
		if dp <= 0:
			return
		
		bout = self.calBout(att, vic, self.buffId)
		buffObj = buff.addOrReplace(vic, self.buffId, bout, att)
		if buffObj:
			ratioFirst, ratio = self.configInfo["伤害率"]
			hpFirst = int(dp * ratioFirst / 100)
			hp = int(dp * ratio / 100)
			buffObj.config(hpFirst, hp)

import buff	