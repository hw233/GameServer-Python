# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

ratioList = {
	0: 60,
	1: 45,
	2: 30,
	4: 15
}

ratioMin = min(ratioList.values())

#导表开始
class Perform(CustomPerform):
	id = 1312
	name = "断月式"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,SLV:SLV/60+3
	targetCountMax = 4
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 5,
	}
	speRatio = 100
#导表结束

	def calDamageRatio(self, att, vic, vicCast, targetCount):
		return ratioList.get(vic.attackedIdx, ratioMin)
			