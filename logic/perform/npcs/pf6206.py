# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6206
	name = "祸水滔天"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 5
	bout = 1
	damage = lambda self,SLV:SLV*2+20
	power = 100
	buffId = 109
	configInfo = {
		"目标生命比":50,
		"概率":lambda HPRV:10+((100-HPRV)/8),
	}
#导表结束

	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		CustomPerform.afterAttack(self, att, vic, vicCast, dp, targetCount)
		if dp <= 0:
			return
		if vic.isDead():
			return
		if vic.hp * 100 / vic.hpMax > self.configInfo["目标生命比"]:
			return
		if rand(100) >= self.transCode(self.configInfo["概率"], att, vic):
			return
		
		bout = self.calBout(att, vic, self.buffId)
		buff.addOrReplace(vic, self.buffId, bout, att)
		

import buff
		