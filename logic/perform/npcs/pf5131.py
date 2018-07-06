# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5131
	name = "禁神"
	applyList = {
		"破神":True,
	}
	configInfo = {
		"伤害结果加成":25,
	}
#导表结束
#将敌人击倒时，其神佑类技能或效果无效，对拥有神佑、高级神佑的敌人伤害结果增加25%
	def onSetup(self, w):
		self.addFunc(w, "onTargetReceiveDamage", self.onTargetReceiveDamage)
		
	def onTargetReceiveDamage(self, att, vic, dp, attackType):
		if vic.hasApply("神佑") or vic.hasApply("高级神佑"):
			return 0, self.configInfo["伤害结果加成"]
		return None
