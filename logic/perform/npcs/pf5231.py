# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5131 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5231
	name = "高级禁神"
	applyList = {
		"破神":True,
	}
	configInfo = {
		"伤害结果加成":35,
	}
#导表结束