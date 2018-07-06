# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5114 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5214
	name = "高级不意"
	configInfo = {
		"概率":50,
		"伤害":30,
	}
#导表结束