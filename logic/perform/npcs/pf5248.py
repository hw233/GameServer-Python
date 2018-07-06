# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5148 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5248
	name = "高级辛金"
	configInfo = {
		"概率":30,
	}
#导表结束