# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5112 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5212
	name = "高级叠刃"
	configInfo = {
		"概率":30,
		"伤害":50,
	}
#导表结束
