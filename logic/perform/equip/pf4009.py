# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RevivePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4009
	name = "风起鹤归"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	consumeList = {
		"愤怒": 120,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = min(vic.hpMax * 50 / 100, vic.level * 20)
		return dp