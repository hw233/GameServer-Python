# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4001
	name = "仰聆玉章"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	consumeList = {
		"愤怒": 60,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = min(vic.hpMax * 18 / 100, vic.level * 10)
		return dp