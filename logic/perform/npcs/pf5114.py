# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5114
	name = "不意"
	configInfo = {
		"概率":40,
		"伤害":30,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		self.addFunc(w, "onPerform", self.doubleAttack)
		self.addFunc(w, "onPhyAttack", self.doubleAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if vic is vicCast:
			self.hp = dp * self.configInfo["伤害"] / 100
			
	def doubleAttack(self, att, vicCast, attackType):
		if not hasattr(self, "hp"):
			return
		
		hp = self.hp
		del self.hp

		if att.isDead():
			return
		if rand(100) >= self.configInfo["概率"]:
			return
		
		targetList = []
		for w in att.getEnemyList():
			if w is vicCast:
				continue
			targetList.append(w)
			
		if not targetList:
			return
		vic = targetList[0]
		vic.addHP(-hp, att)
		self.performSay(att)
		
from common import *