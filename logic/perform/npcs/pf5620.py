# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5620
	name = "苦僧之徒"
	configInfo = {
		"次数":1,
	}
#导表结束

	def onSetup(self, w):
		self.setApply(w, "弹跳次数", self.configInfo["次数"])

	