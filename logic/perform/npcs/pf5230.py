# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5130 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5230
	name = "高级复生"
	configInfo = {
		"概率":lambda LV,con:0.6*LV/con,
		"生命":100,
		"限制":(10,20),
	}
#导表结束