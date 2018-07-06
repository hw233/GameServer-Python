# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1333
	name = "无畏"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
		"符能": 40,
	}
	speRatio = 100
#导表结束
	breakSeal = True # 打破封印限制

	def calDamageRatio(self, att, vic, vicCast, targetCount):
		'''计算伤害率
		'''
		if att.inSeal():
			return 150
		return 100
