# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5612
	name = "万蚕金钵"
	configInfo = {
		"双倍概率":70,
		"回复概率":30,
		"生命":60,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "invertDamage", self.invertDamage)
		self.addFunc(w, "onTargetReceiveDamage", self.onTargetReceiveDamage)

	def invertDamage(self, att, vic, dp, attackType):
		if hasattr(self, "hasDone"):
			del self.hasDone
			return
		if vic.attackedIdx != 0: # 不是主目标
			return None
		if rand(100) >= self.configInfo["回复概率"]:
			return None
		return dp * self.configInfo["生命"] / 100
	
	def onTargetReceiveDamage(self, att, vic, dp, attackType):
		if vic.attackedIdx != 0: # 不是主目标
			return None
		if rand(100) >= self.configInfo["双倍概率"]:
			return None
		
		self.hasDone = True
		return 0, 100
			
			
from common import *
