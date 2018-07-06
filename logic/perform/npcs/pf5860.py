# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5820 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5860
	name = "高级封印"
	configInfo = {
		"封印命中":5,
	}
#导表结束