# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import SealPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6205
	name = "迷魂咒"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 2
	buffId = 109
	hitRatio = 100
#导表结束
#必中，封5回合，目标选择次序：未封印状态-速度高，若目标全被封，则对速度最高的使用

	def customPerformTargetList(self, att, vicCast, targetCount):
		targetList = att.getEnemyList()
		if not targetList:
			return [vicCast,]
		
		targetList.sort(key=self.sortKey, reverse=True)
		return targetList[:targetCount]

	def sortKey(self, w):
		if buff.has(w, self.buffId):
			hasBuff = 1
		else:
			hasBuff = 0
		print "sortKey %s" % w.name, -hasBuff, w.getSpeAll()
		return -hasBuff, w.getSpeAll()

import buff