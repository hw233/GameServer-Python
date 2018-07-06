# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RevivePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4008
	name = "洗尽尘缘"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	consumeList = {
		"愤怒": 90,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = min(vic.hpMax * 20 / 100, vic.level * 10)
		return dp