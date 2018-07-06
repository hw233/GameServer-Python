# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5622
	name = "佛门庇护"
	configInfo = {
		"概率":50,
	}
#导表结束
#玩家触发洗髓易筋的“救赎”效果时，有一定几率不清除“救赎”状态
	def onSetup(self, w):
		self.setApply(w, "PF5622Ratio", self.configInfo["概率"])