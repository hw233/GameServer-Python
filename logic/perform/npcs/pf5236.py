# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5136 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5236
	name = "高级清心"
	configInfo = {
		"概率":lambda LV,con:10-(con-10)/(LV+1),
	}
#导表结束