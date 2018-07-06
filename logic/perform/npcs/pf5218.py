# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5118 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5218
	name = "高级反击"
	configInfo = {
		"概率":40,
	}
#导表结束