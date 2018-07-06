# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5138 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5238
	name = "高级不死"
	configInfo = {
		"概率":40,
	}
#导表结束