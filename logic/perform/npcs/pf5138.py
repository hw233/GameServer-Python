# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5138
	name = "不死"
	configInfo = {
		"概率":25,
	}
#导表结束
#死亡时，有25的几率剩余1点生命值，与神佑或高级神佑共存时无效

	def onSetup(self, w):
		self.addFunc(w, "onRevive", self.onRevive)
		
	def onRevive(self, vic, att):
		if vic.hasApply("神佑") or vic.hasApply("高级神佑"):
			return
		ratio = self.transCode(self.configInfo["概率"], vic, att)
		if rand(100) < ratio:
			vic.addHP(1)
			
from common import *
