# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5139 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5239
	name = "高级回生"
	configInfo = {
		"生命":25,
	}
#导表结束