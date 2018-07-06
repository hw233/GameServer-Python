# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5201
	name = "高级锋锐"
#导表结束

	def setup(self, who):
		self.addApply(who, "phyCritRatio", 20)