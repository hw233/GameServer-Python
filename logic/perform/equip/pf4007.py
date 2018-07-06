# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RevivePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4007
	name = "金灶仙桃"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	consumeList = {
		"愤怒": 60,
	}
#导表结束


	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = 150
		return dp