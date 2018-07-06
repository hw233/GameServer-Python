# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5153 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5253
	name = "高级舍身"
	configInfo = {
		"伤害":lambda LV:LV*5+10,
	}
#导表结束