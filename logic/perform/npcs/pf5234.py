# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5134 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5234
	name = "高级震慑"
	bout = 2
	buffId = 244
	configInfo = {
		"概率":lambda LV,mag:(mag-10)/(LV+1)*2,
	}
#导表结束