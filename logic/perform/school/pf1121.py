# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1121
	name = "神通符法"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
		"符能": 10,
	}
	speRatio = 100
	configInfo = {
		"概率":50,
	}
#导表结束

	def afterPerform(self, att, vicCast):
		CustomPerform.afterPerform(self, att, vicCast)
		if hasattr(self, "moveDone"):
			del self.moveDone

	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		CustomPerform.afterAttack(self, att, vic, vicCast, dp, targetCount)
		
		if hasattr(self, "moveDone"):
			return
		if dp <= 0:
			return
		if not att.inWar() or not vic.inWar():
			return
		if rand(100) >= self.configInfo["概率"]:
			return
		
		if not self.tryGetBuff(att, vic):
			self.tryRemoveBuff(att, vic)
		elif not self.tryRemoveBuff(att, vic):
			self.tryGetBuff(att, vic)
			
		if hasattr(self, "moveDone"):
			for func in att.getFuncList("onMoveDone"):
				func(att, vic, vicCast, dp, self.getAttackType())
				
	def tryGetBuff(self, att, vic):
		'''对方一个正面状态转移给自己
		'''
		for lst in vic.buffList.values():
			for bfObj in shuffleList(lst):
				if not bfObj:
					continue
				if bfObj.type not in (BUFF_TYPE_BUFF,):
					continue
				buff.remove(vic, bfObj.id)
				buff.fork(att, bfObj)
				self.moveDone = True
				return 1

		return 0
	
	def tryRemoveBuff(self, att, vic):
		'''自身一个负面状态转移给对方
		'''
		for lst in att.buffList.values():
			for bfObj in shuffleList(lst):
				if not bfObj:
					continue
				if bfObj.type not in (BUFF_TYPE_DEBUFF, BUFF_TYPE_SEAL,):
					continue
				buff.remove(att, bfObj.id)
				buff.fork(vic, bfObj)
				self.moveDone = True
				return 1

		return 0
				
				
from common import *
from buff.defines import *
import buff

