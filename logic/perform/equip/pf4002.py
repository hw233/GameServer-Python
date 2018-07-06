# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4002
	name = "折节死生"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	consumeList = {
		"愤怒": 90,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = min(vic.hpMax * 25 / 100, vic.level * 15)
		return dp