# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5126 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5226
	name = "高级化生"
	configInfo = {
		"生命":20,
		"上限":lambda LV:LV*6,
	}
#导表结束