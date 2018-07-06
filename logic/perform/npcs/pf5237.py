# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5137 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5237
	name = "高级大义"
	applyList = {
		"禁止逃跑":True,
	}
	configInfo = {
		"概率":10,
	}
#导表结束