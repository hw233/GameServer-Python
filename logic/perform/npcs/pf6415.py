# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6415
	name = "物免回血"
	configInfo = {
		"回血率加成":60,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		
	def onAbsorb(self, att, vic, dp, attackType):
		if len(vic.war.teamList[TEAM_SIDE_2]) == 1: #只剩一个人就不触发了
			return dp
		if attackType.attackType not in phyAttackTypeList:
			return dp
		value = dp * self.configInfo["回血率加成"] / 100
		vic.addHP(value)
		return 0

from war.defines import *