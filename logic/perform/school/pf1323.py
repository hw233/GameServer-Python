# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

timesList = (
	(70, 2),
	(50, 3),
	(40, 4),
	(30, 5),
	(10, 6),
	(0, 7),
)

#导表开始
class Perform(CustomPerform):
	id = 1323
	name = "横扫千军"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 2
	damage = lambda self,SLV:SLV*2+20
	power = 50
	consumeList = {
		"真气": lambda SLV:SLV*1.2+50,
		"符能": 50,
	}
	buffId = 123
	speRatio = 100
#导表结束

	def validPerform(self, att, needTips):
		'''检查施法
		'''
		if att.hasApply("已复活"):
			if needTips:
				message.tips(att.getPID(), "被复活当前回合无法使用")
			return False
		return CustomPerform.validPerform(self, att, needTips)

	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		vic = targetList[0]
		att.war.rpcWarPerform(att, self.getMagId(), vic)

		hitTimes = self.calHitTimes(att)
		for i in xrange(hitTimes):
			att.war.rpcWarPerform(att, self.getMagId(), vic)
			self.attack(att, vic, vicCast, 1)
			if vic.isDead():
				break
			if att.isDead():
				break
		
		if att.inWar():
			bout = self.calBout(att, att, self.buffId)
			buff.addOrReplace(att, self.buffId, bout, att)
			
	def calHitTimes(self, att):
		v = att.hp * 100 / att.hpMax
		for ratio, times in timesList:
			if v >= ratio:
				return times
		return 1

import buff
import message
