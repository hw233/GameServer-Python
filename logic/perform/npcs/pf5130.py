# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5130
	name = "复生"
	configInfo = {
		"概率":lambda LV,con:0.6*LV/con,
		"生命":60,
		"限制":(10,20),
	}
#导表结束
#战斗中死亡时，有0.6*等级/体质的几率复活并回复60%生命，概率最大为20%，最小为10%，与鬼魂或高级鬼魂共存时无效

	def onSetup(self, w):
		self.addFunc(w, "onRevive", self.onRevive)
		self.setApply(w, self.name, True)
		
	def onRevive(self, vic, att):
		ratio = int(100 * self.transCode(self.configInfo["概率"], vic, att))
		ratioMin, ratioMax = self.configInfo["限制"]
		if ratio < ratioMin:
			ratio = ratioMin
		elif ratio > ratioMax:
			ratio = ratioMax
		if rand(100) < ratio:
			hp = vic.hpMax * self.configInfo["生命"] / 100
			self.performSay(vic)
			vic.addHP(hp)
			
			
from common import *
