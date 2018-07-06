# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5117 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5217
	name = "高级连斩"
	configInfo = {
		"概率":40,
		"伤害结果加成":-15,
	}
#导表结束