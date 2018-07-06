# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5140 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5240
	name = "高级益气"
	configInfo = {
		"真气":25,
	}
#导表结束