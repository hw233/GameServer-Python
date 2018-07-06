# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1613
	name = "索命梵音"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 60
	consumeList = {
		"真气": lambda SLV:SLV*1.2+30,
		"符能": 20,
	}
	speRatio = 60
#导表结束

	def afterPerform(self, att, vicCast):
		CustomPerform.afterPerform(self, att, vicCast)
		
		# 给hp最低的加血
		targetObj = None
		for w in att.getFriendList():
			if targetObj and targetObj.hp < w.hp:
				continue
			targetObj = w
		
		if not targetObj:
			return

		targetCount = 1
		damRatio = self.calDamageRatio(att, targetObj, targetObj, targetCount)
		dp = self.calCure(att, targetObj, targetObj, damRatio)
		targetObj.addHP(dp, att)
		
		# 随机给另一个加血		
		info = att.hasApply("PF5618Info")
		if not info:
			return
		if rand(100) >= info["概率"]:
			return
		for w in att.getFriendList():
			if w is att:
				continue
			if w is targetObj:
				continue
			hp = dp * info["生命"] / 100
			w.addHP(hp, att)
			return
				
	def calCure(self, att, vic, vicCast, damRatio):
		magDam = int(self.transCode("SLV*2+20", att, vic))
		dp = att.calCure(vic, magDam, 70, damRatio, self.getAttackType())
		return dp
	

from common import *