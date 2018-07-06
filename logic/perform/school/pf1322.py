# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1322
	name = "乘胜追击"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	targetCountMax = 3
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
		"符能": 20,
	}
	speRatio = 100
#导表结束

	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		vic = targetList[0]
		att.war.rpcWarPerform(att, self.getMagId(), vic)

		for i in xrange(self.targetCountMax):
			att.war.rpcWarPerform(att, self.getMagId(), vic)
			self.attack(att, vic, vicCast, 1)
			if att.isDead():
				break
			if not vic.isDead():
				break
			vic = att.getEnemyTarget()
			if not vic:
				break
