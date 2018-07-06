# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1331
	name = "流星"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
		"符能": 10,
	}
	speRatio = 100
#导表结束

	def calDamageRatio(self, att, vic, vicCast, targetCount):
		'''计算伤害率
		'''
		if vic.hp > vic.hpMax * 0.9:
			return 120
		return 100