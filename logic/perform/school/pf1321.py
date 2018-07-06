# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

ratioList = {
	0: 55,
	1: 65,
	2: 75,
}

ratioMin = min(ratioList.values())

#导表开始
class Perform(CustomPerform):
	id = 1321
	name = "势如破竹"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 2
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
	}
	recoverList = {
		"符能": 20,
	}
	buffId = 123
	speRatio = 100
#导表结束

	def validPerform(self, att, needTips):
		'''检查施法
		'''
		if att.hp <= int(att.hpMax * 0.5):
			if needTips:
				message.tips(att.getPID(), "只能在#C04当前生命值>50%#n时使用")
			return False
		return CustomPerform.validPerform(self, att, needTips)
	
	def calDamageRatio(self, att, vic, vicCast, targetCount):
		return ratioList.get(vic.attackedIdx, ratioMin)

	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		vic = targetList[0]
		att.war.rpcWarPerform(att, self.getMagId(), vic)

		for idx in xrange(3):
			vic.attackedIdx = idx # 被攻击序号
			att.war.rpcWarPerform(att, self.getMagId(), vic)
			self.attack(att, vic, vicCast, 1)
			if vic.isDead():
				break
			if att.isDead():
				break
		
		if att.inWar():
			bout = self.calBout(att, att, self.buffId)
			buff.addOrReplace(att, self.buffId, bout, att)


import buff
import message
