# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5125 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5225
	name = "高级坚韧"
	applyList = {
		"免疫暴击":True,
	}
	configInfo = {
		"概率":10,
	}
#导表结束