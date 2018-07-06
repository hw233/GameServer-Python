# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5135 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5235
	name = "高级眩晕"
	bout = 1
	buffId = 245
	configInfo = {
		"概率":lambda LV,str:(str-10)/(LV+1)*2,
	}
#导表结束