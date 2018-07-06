# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

ratioList = {
	1: 70,
	2: 50,
	3: 30,
	4: 10,
}

#导表开始
class Perform(CustomPerform):
	id = 1133
	name = "先天正气诀"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	targetCountMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1+40,
		"符能": 50,
	}
	speRatio = 100
#导表结束

	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		CustomPerform.afterAttack(self, att, vic, vicCast, dp, targetCount)
		if dp > 0 and not att.isDead() and not hasattr(self, "isContinue"):
			self.isContinue = True
			self.continuePerform(att, vic)
			del self.isContinue
		
	def continuePerform(self, att, vic):
		'''追击
		'''
		warObj = att.war
		idxList = ratioList.keys()
		idxList.sort()
		excludeList = [vic] # 每个敌人只能追击一次
		for idx in idxList:
			ratio = ratioList[idx]
			if rand(100) >= ratio:
				return

			nextVic = self._getNextTarget(att, excludeList)
			if not nextVic:
				return
			excludeList.append(nextVic)

			warObj.printDebugMsg("\t[%s]使用[%s]追击[%s],概率%d" % (att.name, self.name, nextVic.name, ratio))
			warObj.rpcWarPerform(att, self.getMagId(idx), nextVic)
			self.attack(att, nextVic, vic, 1)
			
			if att.isDead():
				return

	def _getNextTarget(self, att, excludeList):
		targetList = att.getEnemyList()
		for vic in excludeList:
			if vic in targetList:
				targetList.remove(vic)
		if not targetList:
			return None
		return targetList[0]

from common import *

