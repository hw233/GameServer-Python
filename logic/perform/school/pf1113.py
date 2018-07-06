# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RemotePhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1113
	name = "万剑归一"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,SLV:SLV/35+3
	targetCountMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
		"符能": 40,
	}
	speRatio = 100
#导表结束

	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		targetCount = len(targetList)
		
		att.war.rpcWarPerform(att, self.getMagId(), targetList)
		for idx, vic in enumerate(targetList):
			if vic.isDead():
				continue
			vic.attackedIdx = idx # 被攻击序号
			self.attack(att, vic, vicCast, targetCount)
			if att.isDead():
				break
			
			#对主目标追加一次额外伤害
			if idx == 0 and not vic.isDead():
				self.attack(att, vic, vicCast, targetCount)