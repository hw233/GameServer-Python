# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5145 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5245
	name = "高级甲木"
	configInfo = {
		"概率":30,
	}
#导表结束