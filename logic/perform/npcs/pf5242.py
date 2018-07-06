# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5142 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5242
	name = "高级乘胜"
	configInfo = {
		"伤害率":100,
	}
#导表结束