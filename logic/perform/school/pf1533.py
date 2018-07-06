# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1533
	name = "翻江倒海"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 99
	damage = lambda self,SLV:SLV*2+20
	power = 25
	consumeList = {
		"真气": lambda SLV:SLV*1.2+30,
		"符能": 50,
	}
	speRatio = 108
#导表结束

	def calDamageRatio(self, att, vic, vicCast, targetCount):
		return 100
