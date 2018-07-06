# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RevivePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4010
	name = "海上明月"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	consumeList = {
		"愤怒": 120,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = min(vic.hpMax * 10 / 100, vic.level * 10)
		return dp

	def checkCastTarget(self, att, vicCast):
		if not vicCast:
			message.tips(att.getPID(), "没有指定作用目标")
			return None
		if vicCast.side != att.side:
			message.tips(att.getPID(), "只能作用于已方")
			return None
		for w in vicCast.getFriendList(True):
			if w.isPet():
				continue
			if w.isDead():
				return w
		#走到这里表示没有人死亡
		message.tips(att.getPID(), "目标不需要复活")
		return None

import message