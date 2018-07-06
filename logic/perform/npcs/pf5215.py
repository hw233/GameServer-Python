# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5115 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5215
	name = "高级镜反"
	configInfo = {
		"概率":40,
		"伤害":25,
	}
#导表结束