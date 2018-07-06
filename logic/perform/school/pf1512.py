# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1512
	name = "噬骨魔火"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
		"符能": 10,
	}
	speRatio = 101
	configInfo = {
		"伤害率":{0:55,1:60},
		"生命值限制":70,
	}
#导表结束

	def validPerform(self, att, needTips):
		'''检查施法
		'''
		ratio = att.hasApply("PF1512_HPLimit")
		if not ratio:
			ratio = self.configInfo["生命值限制"]
		if att.hp <= int(att.hpMax * ratio / 100):
			if needTips:
				message.tips(att.getPID(), "只能在#C04当前生命值>{}%#n时使用".format(ratio))
			return False
		return CustomPerform.validPerform(self, att, needTips)
	
	def calDamageRatio(self, att, vic, vicCast, targetCount):
		ratioList = self.configInfo["伤害率"]
		ratioMin = min(ratioList.values())
		return ratioList.get(vic.attackedIdx, ratioMin)

	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		vic = targetList[0]
		ratioList = self.configInfo["伤害率"]
		for idx in xrange(len(ratioList)):
			vic.attackedIdx = idx # 被攻击序号
			att.war.rpcWarPerform(att, self.getMagId(), vic)
			self.attack(att, vic, vicCast, 1)
			if vic.isDead():
				break
			if att.isDead():
				break


import message