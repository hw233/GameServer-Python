# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5120 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5220
	name = "高级刺甲"
	configInfo = {
		"反弹概率":50,
		"伤害率":30,
	}
#导表结束