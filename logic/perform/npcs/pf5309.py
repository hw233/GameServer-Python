# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5309
	name = "凤舞回元"
	configInfo = {
		"转化伤害":10,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if vic.attackedIdx != 0: # 不是主目标
			return None

		friendList = att.getFriendList()
		if not friendList:
			return
		friendList.sort(key=lambda w: w.hp)
		w = friendList[0]
		hp = dp * self.configInfo["转化伤害"] / 100
		w.addHP(hp, att)
