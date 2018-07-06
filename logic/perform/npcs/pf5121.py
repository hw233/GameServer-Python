# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5121
	name = "无畏"
	applyList = {
		"免疫反弹":True,
	}
	configInfo = {
		"物理伤害结果加成":5,
	}
#导表结束
#物理攻击不会受到敌方反震、刺甲的反弹效果，物理伤害提高5%

	def onSetup(self, w):
		self.addApply(w, "物理伤害结果加成", self.configInfo["物理伤害结果加成"])
