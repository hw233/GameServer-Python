# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5609 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5621
	name = "先圣之灵"
	configInfo = {
		"回复生命":10,
	}
#导表结束