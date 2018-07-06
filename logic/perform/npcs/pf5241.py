# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5141 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5241
	name = "高级妙法"
	configInfo = {
		"概率":10,
		"符能":15,
	}
#导表结束