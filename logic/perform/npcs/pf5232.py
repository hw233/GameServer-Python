# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5132 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5232
	name = "高级破封"
	configInfo = {
		"概率":100,
	}
#导表结束