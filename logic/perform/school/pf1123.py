# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RemotePhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1123
	name = "天师符法"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,LV:LV/35+3
	targetCountMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
		"符能": 40,
	}
	speRatio = 100
#导表结束

	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		CustomPerform.afterAttack(self, att, vic, vicCast, dp, targetCount)
		if dp > 0 and att.inWar() and vic.inWar():
			self.removeBuff(att, vic)
				
	def removeBuff(self, att, vic):
		'''驱散对方被攻击目标随机一个正面状态
		'''
		for lst in vic.buffList.values():
			for bfObj in lst:
				if not bfObj:
					continue
				if bfObj.type not in (BUFF_TYPE_BUFF,):
					continue
				buff.remove(vic, bfObj.id)
				return
	
from buff.defines import *
import buff
